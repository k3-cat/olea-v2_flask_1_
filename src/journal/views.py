from flask import jsonify

from auth import login_required, permission_required
from exts import db

from . import journal_bp
from .errors import NonExistedObj
from .forms import Apply, Transfer
from .models import Apl, Txn


@journal_bp.route('/apply', methods=['POST'])
@login_required
def apply():
    form = Apply()
    apl = Apl(reason=form.reason.data, amount=form.amount.data)
    db.session.add(apl)
    db.session.commit()
    return jsonify({'id': apl.id})


@journal_bp.route('/get_last_txn', methods=['GET'])
def get_last_txn():
    last_txn = Txn.query.order_by(Txn.timestamp.desc()).first()
    return jsonify({'id': last_txn.id})


@journal_bp.route('/transfer', methods=['POST'])
@permission_required(perm='journal.transfer')
def transfer():
    form = Transfer()
    apl = Apl.query.get(form.aid.data)
    if not apl:
        raise NonExistedObj(cls=Apl)
    txn = Txn(debit=0,
              credit=apl.amount,
              reason=apl.reason,
              previous_id=form['pervious_id'])
    db.session.add(txn)
    db.session.delete(apl)
    db.session.commit()
    return jsonify({'id': txn.id})
