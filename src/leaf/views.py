from flask import (Response, current_app, g, jsonify, request,
                   stream_with_context)

from auth import login_required
from exts import db
from exts.sqlalchemy_ import UNIQUE_VIOLATION, IntegrityError
from pink.utils import query_pink
from proj.utils import query_proj

from . import leaf_bp
from .errors import DuplicateLeaf, NoFileSubmited
from .forms import Pick, SingleLeaf
from .models import Leaf
from .utils import query_leaf


@leaf_bp.route('/pick', methods=['POST'])
@login_required
def pick():
    form = Pick()
    leaf = Leaf(proj=query_proj(form['proj']),
                dep=form['dep'],
                role=form['role'],
                pink=query_pink(g.pink_id))
    db.session.add(leaf)
    try:
        db.session.commit()
    except IntegrityError as e:
        if e.orig.pgcode == UNIQUE_VIOLATION:
            raise DuplicateLeaf()
        raise
    return jsonify({'id': leaf.id})


@leaf_bp.route('/drop', methods=['POST'])
@login_required
def drop():
    leaf = query_leaf(SingleLeaf()['leaf'])
    leaf.drop()
    db.session.add(leaf)
    db.session.commit()
    return jsonify({})


@leaf_bp.route('/redo', methods=['GET'])
@login_required
def redo():
    leaf = query_leaf(SingleLeaf()['leaf'])
    leaf.redo()
    db.session.add(leaf)
    db.session.commit()
    return jsonify({})


@leaf_bp.route('/submit/<string:id_>', methods=['POST'])
@login_required
def submit(id_: str):
    if 'mango' not in request.files:
        raise NoFileSubmited()
    leaf = query_leaf(id_)
    mango = leaf.submit(f=request.files['mango'])
    db.session.add(mango)
    db.session.commit()
    return jsonify({'id': mango.id})


@leaf_bp.route('/download/<string:id_>', methods=['GET'])
@login_required
def download(id_: str):
    leaf = query_leaf(id_)
    mango_id, filename = leaf.download()

    def generate(mango_id):
        with open(f'{current_app.root_path}/{mango_id}', 'rb') as f:
            while True:
                block = f.read(2 * 1024)
                if block:
                    yield block
                else:
                    return

    return Response(
        stream_with_context(generate(mango_id)),
        headers={'Content-Disposition': f'attachment; filename={filename}'})
