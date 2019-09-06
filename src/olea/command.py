import datetime
from hashlib import sha3_256

import click
from flask.cli import with_appcontext

from exts import db


def register_commands(app):
    """Register Click commands."""
    @click.command("init-db")
    @with_appcontext
    def init_db_command():
        """Clear existing data and create new tables."""
        db.drop_all()
        db.create_all()
        db.engine.execute("INSERT INTO pink (id, name, active) "
                          f"VALUES ('{'0' * 9}', 'SYSTEM', False);")
        now = datetime.datetime.utcnow()
        txn_info = f'None_0_0_init_{"0" * 9}_{now}'
        id_ = sha3_256(txn_info.encode('utf-16')).hexdigest()
        db.engine.execute(
            "INSERT INTO txn (id, previous_id, debit, credit, reason, pink_id, timestamp) "
            f"VALUES ('{id_}', '{id_}', 0, 0, 'init',  '{'0' * 9}', '{now}');")
        click.echo('\nDatabase Initialized')

    app.cli.add_command(init_db_command)
