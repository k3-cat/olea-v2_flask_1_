from typing import List

from flask import g, jsonify

from auth import ta
from exts import db, mailgun
from exts.sqlalchemy_ import UNIQUE_VIOLATION, IntegrityError

from . import pink_bp
from .errors import DuplicatePink
from .forms import Create, SinglePink, UpdateInfo
from .models import Pink
from .pwd_tools import generate_pwd
from .utils import get_pink


@pink_bp.route('/all', methods=['GET'])
@ta.login_required
def all_pinks():
    pinks: List[Pink] = Pink.query.filter_by(active=True).all()
    return jsonify([pink.to_dict(lv=0) for pink in pinks])


@pink_bp.route('/<string:id_>', methods=['GET'])
@ta.login_required
def get_pink_(id_: str):
    pink = get_pink(id_)
    return jsonify(pink.to_dict(lv=1))


@pink_bp.route('/info', methods=['GET'])
@ta.login_required
def info():
    pink = get_pink(g.pink_id)
    return jsonify(pink.to_dict(lv=1))


@pink_bp.route('/update_info', methods=['POST'])
@ta.login_required
def update_info():
    form = UpdateInfo()
    pink = get_pink(g.pink_id)
    dirty = False
    if form['qq']:
        dirty = True
        pink.qq = str(form['qq'])
    if form['line']:
        dirty = True
        pink.line = form['line']
    if form['email']:
        dirty = True
        pink.email = form['email']
    if dirty:
        db.session.add(pink)
        db.session.commit()
    return 'True'


# europaea
@pink_bp.route('/create', methods=['POST'])
def create():
    form = Create()
    pink: Pink = Pink(name=form.name.data,
                      qq=form.qq.data,
                      line=form.line.data,
                      email=form.email.data,
                      deps=form.deps.data)
    pwd = generate_pwd()
    pink.pwd = pwd
    db.session.add(pink)
    try:
        db.session.commit()
    except IntegrityError as e:
        if e.orig.pgcode == UNIQUE_VIOLATION:
            raise DuplicatePink()
        raise
    mailgun.send(subject='初次见面, 这里是olea',
                 to=(pink.email, ),
                 template='new_pink',
                 values={
                     'name': pink.name,
                     'pwd': pwd
                 })
    return jsonify({'id': pink.id})


# europaea
@pink_bp.route('/reset_pwd', methods=['POST'])
def reset_pwd():
    pink = get_pink(SinglePink()['pink'])
    pwd = generate_pwd()
    pink.pwd = pwd
    mailgun.send(subject='新的口令',
                 to=[pink.email],
                 template='reset_pink',
                 values={
                     'name': pink.name,
                     'pwd': pwd
                 })
    db.session.add(pink)
    db.session.commit()
    return jsonify({})


# europaea
@pink_bp.route('/deactive')
def deactive():
    pink = get_pink(SinglePink()['pink'], europaea=True)
    pink.active = False
    db.session.add(pink)
    for token in pink.tokens:
        db.session.delete(token)
    db.session.commit()
    return jsonify({})
