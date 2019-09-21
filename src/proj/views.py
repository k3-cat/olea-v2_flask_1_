from __future__ import annotations

from typing import TYPE_CHECKING, List

from flask import g, jsonify

from auth import login_required, permission_required
from exts import db
from exts.sqlalchemy_ import UNIQUE_VIOLATION, IntegrityError

from . import proj_bp
from .errors import DuplicateObj
from .forms import Create, EditNote, InitRoles, SingleProj
from .models import Proj
from .utils import query_proj

if TYPE_CHECKING:
    from .models import Progress


@proj_bp.route('/all', methods=['GET'])
@login_required
def all_projs():
    projs: List[Proj] = Proj.query.filter_by(finish_at=None).all()
    return jsonify([proj.to_dict(lv=0) for proj in projs])


@proj_bp.route('/<string:id_>', methods=['GET'])
@login_required
def get_proj(id_: str):
    proj = query_proj(id_)
    return jsonify(proj.to_dict(lv=1))


@proj_bp.route('/edit_note', methods=['POST'])
@login_required
def edit_note():
    form = EditNote()
    proj = query_proj(form['proj'])
    proj.set_note(form['note'])
    db.session.add(proj)
    db.session.commit()
    return jsonify({})


@proj_bp.route('/book', methods=['POST'])
@login_required
def book():
    proj = query_proj(SingleProj()['proj'])
    progress: Progress = proj.progress
    progress.book(pink_id=g.pink_id)
    db.session.add(progress)
    db.session.commit()
    return jsonify({})


@proj_bp.route('/cancll_booking', methods=['POST'])
@login_required
def cancll_booking():
    proj = query_proj(SingleProj()['proj'])
    progress: Progress = proj.progress
    progress.canell_booking(pink_id=g.pink_id)
    db.session.add(progress)
    db.session.commit()
    return jsonify({})


@proj_bp.route('/init_roles', methods=['POST'])
@permission_required(perm='proj.init_roles')
def init_roles():
    form = InitRoles()
    proj = query_proj(form['proj'])
    progress: Progress = proj.progress
    progress.set_roles(form['roles'])
    db.session.add(progress)
    db.session.commit()
    return jsonify({})


@proj_bp.route('/create', methods=['POST'])
@permission_required(perm='proj.create')
def create():
    form = Create()
    proj: Proj = Proj(base=form['base'],
                      pub_date=form['pub_date'],
                      cat=form['cat'],
                      note=form['note'],
                      suff=form['suff'])
    db.session.add(proj)
    try:
        db.session.commit()
    except IntegrityError as e:
        if e.orig.pgcode == UNIQUE_VIOLATION:
            raise DuplicateObj(obj=proj)
        raise
    return jsonify({'id': proj.id})
