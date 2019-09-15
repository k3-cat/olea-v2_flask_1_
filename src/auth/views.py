from flask import g, jsonify

from exts import db
from pink.models import Pink
from pink.utils import query_pink

from . import auth_bp, login_required
from .errors import InvalidCredential
from .forms import Login, SetPubKey, SetPwd
from .models import Lemon
from .utils import query_duck


@auth_bp.route('/login', methods=['POST'])
def login():
    form = Login()
    pink: Pink = Pink.query.filter_by(active=True, name=form.name.data).first()
    if not pink or not pink.verify_pwd(form.pwd.data):
        raise InvalidCredential()
    lemons = Lemon.query.filter_by(pink_id=pink.id).all()
    if len(lemons) >= 3:
        db.session.delete(lemons[0])
    lemon = Lemon(pink_id=pink.id)
    db.session.add(lemon)
    db.session.commit()
    return jsonify({'pink_id': pink.id, 'key': lemon.key})


@auth_bp.route('/revork', methods=['POST'])
@login_required
def revork():
    db.session.delete(g.lemon)
    db.session.commit()
    return jsonify({})


@auth_bp.route('/revork_all', methods=['POST'])
@login_required
def revork_all():
    for lemon in query_pink(g.pink_id).lemons:
        db.session.delete(lemon)
    db.session.commit()
    return jsonify({})


@auth_bp.route('/set_pwd', methods=['POST'])
@login_required
def set_pwd():
    form = SetPwd()
    pink: Pink = query_pink(g.pink_id)
    pink.pwd = form['pwd']
    db.session.add(pink)
    db.session.commit()
    return jsonify({})


@auth_bp.route('/set_pub_key', methods=['POST'])
@login_required
def set_pub_key():
    form = SetPubKey()
    duck = query_duck(g.pink_id)
    duck.set_pub_key(form['pub_key'])
    db.session.add(duck)
    db.session.commit()
    return jsonify({})
