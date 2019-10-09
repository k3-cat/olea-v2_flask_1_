from __future__ import annotations

import os
from typing import TYPE_CHECKING

import boto3

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
        self.space = app.config['SPACE_NAME']
        self.session = boto3.session.Session()
        self.client = self.session.client(
            's3',
            region_name=app.config['SPACE_REGION'],
            endpoint_url=
            f'https://{app.config["SPACE_REGION"]}.digitaloceanspaces.com',
            aws_access_key_id=app.config['SPACE_KEY'],
            aws_secret_access_key=app.config['SPACE_SECRET'])

        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['storage'] = self

    def upload(self, mango: Mango, path: str) -> bool:
        self.client.upload_file(path, self.space,
                                f'{mango.leaf.proj.id}/{mango.id}')
        return True

    def multi_part_upload(self, mango: Mango, path: str) -> bool:
        self.client.upload_file(path, self.space,
                                f'{mango.leaf.proj.id}/{mango.id}')
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
