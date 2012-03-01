
from datetime import datetime, timedelta
from basesession import Session

session_pool = dict()

class RamSession(Session):

    def __getitem__(self, value_name):
        return session_pool[self.sid].setdefault(value_name, None)

    def __setitem__(self, value_name, value_data):
        session_pool[self.sid][value_name] = value_data

    def initNewSession(self):
        data = dict()
        self.sid = '%s' % id(data)
        session_pool[self.sid] = data
        return self.sid

    def refreshExpiryTime(self):
        session_pool[self.sid]['_expired_at'] = datetime.now() + timedelta(seconds = 10)

    def isInPool(self):
        return session_pool.has_key(self.sid)


def cleaning():
    global session_pool
    session_pool = {k:v for k, v in session_pool.iteritems() if v['_expired_at'] > datetime.now()}

Session.registerImplement(RamSession, cleaning)
