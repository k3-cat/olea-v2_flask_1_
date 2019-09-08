from __future__ import annotations

from typing import TYPE_CHECKING, List

from flask import g, jsonify

from auth import ta
from exts import db
from exts.sqlalchemy_ import UNIQUE_VIOLATION, IntegrityError

from . import proj_bp
from .errors import DuplicateProj
from .forms import Create, EditNote, InitRoles, SingleProj
from .models import Proj
from .utils import get_proj

if TYPE_CHECKING:
    from .models import Progress


@proj_bp.route('/all', methods=['GET'])
@ta.login_required
def all_projs():
    projs: List[Proj] = Proj.query.filter_by(finish_at=None).all()
    return jsonify([proj.to_dict(lv=0) for proj in projs])


@proj_bp.route('/<string:id_>', methods=['GET'])
@ta.login_required
def get_proj_(id_: str):
    proj = get_proj(id_)
    return jsonify(proj.to_dict(lv=1))


@proj_bp.route('/edit_note', methods=['POST'])
@ta.login_required
def edit_note():
    form = EditNote().validate()
    proj = get_proj(form.data['proj'])
    proj.set_note(form.data['note'])
    db.session.add(proj)
    db.session.commit()
    return jsonify({'note': proj.note.split('$|\n', 1)})


@proj_bp.route('/book', methods=['POST'])
@ta.login_required
def book():
    proj = get_proj(SingleProj().validate().data['proj'])
    progress: Progress = proj.progress
    progress.book(pink_id=g.pink_id)
    db.session.add(progress)
    db.session.commit()
    return jsonify({'booking_user': progress.booking_pink})


@proj_bp.route('/cancll_booking', methods=['POST'])
@ta.login_required
def cancll_booking():
    proj = get_proj(SingleProj().validate().data['proj'])
    progress: Progress = proj.progress
    progress.canell_booking(pink_id=g.pink_id)
    db.session.add(progress)
    db.session.commit()
    return jsonify({})


# europaea
@proj_bp.route('/init_roles', methods=['POST'])
def init_roles():
    form = InitRoles().validate()
    proj = get_proj(form.data['proj'])
    progress: Progress = proj.progress
    progress.set_roles(form.data['roles'])
    db.session.add(progress)
    db.session.commit()
    return jsonify({})


# europaea
@proj_bp.route('/create', methods=['POST'])
def create():
    form = Create().validate()
    proj: Proj = Proj(base=form.data['base'],
                      pub_date=form.data['pub_date'],
                      cat=form.data['cat'],
                      note=form.data['note'],
                      suff=form.data['suff'])
    db.session.add(proj)
    try:
        db.session.commit()
    except IntegrityError as e:
        if e.orig.pgcode == UNIQUE_VIOLATION:
            raise DuplicateProj()
        raise
    return jsonify({'id': proj.id})
