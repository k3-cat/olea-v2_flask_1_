from typing import List

from flask import g, jsonify

from auth import login_required, permission_required
from exts import db, mailgun

from . import pink_bp
from .forms import Create, SinglePink, UpdateInfo
from .models import Pink
from .utils import query_pink
from .services import PinkService

@pink_bp.route('/all', methods=['GET'])
@login_required
def all_pinks():
    g.read_only = True
    pinks: List[Pink] = Pink.query.filter_by(active=True).all()
    return jsonify([pink.to_dict(lv=0) for pink in pinks])


@pink_bp.route('/<string:id_>', methods=['GET'])
@login_required
def get_pink(id_: str):
    g.read_only = True
    pink = query_pink(id_)
    return jsonify(pink.to_dict(lv=1))


@pink_bp.route('/info', methods=['GET'])
@login_required
def info():
    g.read_only = True
    pink = query_pink(g.pink_id)
    return jsonify(pink.to_dict(lv=1))


@pink_bp.route('/update_info', methods=['POST'])
@login_required
def update_info():
    form = UpdateInfo()
                          qq=form['qq'],
                      line=form['line'],
                      email=form['email'],
    return 'True'


@pink_bp.route('/create', methods=['POST'])
@permission_required(perm='pink.create')
def create():
    form = Create()
    pink: Pink = Pink(name=form['name'],
                      qq=form['qq'],
                      line=form['line'],
                      email=form['email'],
                      deps=form['deps'])

    return jsonify({'id': pink.id})


@pink_bp.route('/reset_pwd', methods=['POST'])
@permission_required(perm='pink.reset_pwd')
def reset_pwd():
    pink = query_pink(SinglePink()['pink'])

    db.session.add(pink)
    db.session.commit()
    return jsonify({})


@pink_bp.route('/deactive')
@permission_required(perm='pink.deative')
def deactive():
    pink = query_pink(SinglePink()['pink'], europaea=True)
    pink.active = False
    db.session.add(pink)
    for token in pink.tokens:
        db.session.delete(token)
    db.session.commit()
    return jsonify({})
