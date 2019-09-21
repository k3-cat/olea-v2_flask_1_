from __future__ import annotations

import os
from typing import TYPE_CHECKING

from google.cloud import storage

if TYPE_CHECKING:
    from leaf.models import Mango
    from proj.models import Proj


class Storage():
    app = None

    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app) -> None:
        self.app = app
        storage_client = storage.Client.from_service_account_json(
            self.app.config['SERVICE_ACCOUNT_JSON'])
        self.bucket = storage_client.get_bucket(app.config['BUCKET_NAME'])

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['storage'] = self

    def upload(self, mango: Mango, path: str) -> bool:
        blob = self.bucket.blob(f'{mango.leaf.proj.id}/{mango.id}')
        blob.upload_from_filename(path)
        return True

    def download(self, mango: Mango) -> bool:
        filename = f'{self.app.root_path}/{mango.id}'
        if os.path.exists(filename):
            return True
        blob = self.bucket.blob(f'{mango.leaf.proj.id}/{mango.id}')
        blob.download(filename)
        return True

    def real_delete_all(self, proj: Proj) -> None:
        blob = self.bucket.blob(proj.id)
        blob.delete()
