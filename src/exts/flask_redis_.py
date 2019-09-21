import redis


class FlaskRedis():
    def __init__(self, strict=True, **kwargs):
        self._redis_client = None
        self.provider_class = redis.StrictRedis if strict else redis.Redis
        self.provider_kwargs = kwargs

    def init_app(self, app, **kwargs):
        redis_url = app.config['REDIS_URL']
        self.provider_kwargs.update(kwargs)
        self._redis_client = self.provider_class.from_url(
            redis_url, **self.provider_kwargs)

        if not app.config.get('FAKE_REDIS', False):
            from fakeredis import FakeRedis
            self.provider_class = FakeRedis
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['redis'] = self

    def __getattr__(self, name):
        return getattr(self._redis_client, name)

    def __getitem__(self, name):
        return self._redis_client[name]

    def __setitem__(self, name, value):
        self._redis_client[name] = value

    def __delitem__(self, name):
        del self._redis_client[name]
