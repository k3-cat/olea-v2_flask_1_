from flask import g, jsonify

from exts import db
from pink.models import Pink
from pink.utils import get_pink

from . import auth_bp, ta
from .errors import InvalidCredential
from .forms import Login, ModiELemon, SetPwd
from .models import ELemon, Lemon


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
@ta.login_required
def revork():
    db.session.delete(g.lemon)
    db.session.commit()
    return jsonify({})


@auth_bp.route('/revork_all', methods=['POST'])
@ta.login_required
def revork_all():
    for lemon in get_pink(g.pink_id).lemons:
        db.session.delete(lemon)
    db.session.commit()
    return jsonify({})


@auth_bp.route('/set_pwd', methods=['POST'])
@ta.login_required
def set_pwd():
    form = SetPwd()
    pink: Pink = get_pink(g.pink_id)
    pink.pwd = form['pwd']
    db.session.add(pink)
    db.session.commit()
    return jsonify({})


@auth_bp.route('/modi_eleamon', methods=['POST'])
def modi_eleamon():
    form = ModiELemon()
    elemon: ELemon = form['pink'].elemon
    if not elemon:
        pink: Pink = Pink.query.get(form['pink'])
        # ?check
        elemon = ELemon(pink=pink)
    elemon.modi(form['asign'], form['revork'])
    if elemon.perms:
        db.session.add(elemon)
    else:
        db.session.delete(elemon)
    db.session.commit()
    return jsonify({'key': elemon.key})
