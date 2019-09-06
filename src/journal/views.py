from flask import jsonify

from auth import ta
from exts import db

from . import journal_bp
from .errors import AplNotExist
from .forms import Apply, Transfer
from .models import Apl, Txn


@journal_bp.route('/apply', methods=['POST'])
@ta.login_required
def apply():
    form = Apply().validate()
    apl = Apl(reason=form.reason.data, amount=form.amount.data)
    db.session.add(apl)
    db.session.commit()
    return jsonify({'id': apl.id})


@journal_bp.route('/get_last_txn', methods=['GET'])
def get_last_txn():
    last_txn = Txn.query.order_by(Txn.timestamp.desc()).first()
    return jsonify({'id': last_txn.id})


# europaea
@journal_bp.route('/transfer', methods=['POST'])
@ta.login_required
def transfer():
    form = Transfer().validate()
    apl = Apl.query.get(form.aid.data)
    if not apl:
        raise AplNotExist()
    txn = Txn(debit=0,
              credit=apl.amount,
              reason=apl.reason,
              previous_id=form.data['pervious_id'])
    db.session.add(txn)
    db.session.delete(apl)
    db.session.commit()
    return jsonify({'id': txn.id})
