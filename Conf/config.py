class Config(object):

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

#============DB===================
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PASSWORD = None
REDIS_DB = 0
REDIS_HOST_PORT = '%(host)s:%(port)s' % {'host': REDIS_HOST, 'port': REDIS_PORT}
UNLOGIN_SESSION_AGE = 60 * 30
#============DB end===============