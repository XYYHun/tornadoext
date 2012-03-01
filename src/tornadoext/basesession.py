
COOKIES_NAME_SESSION_ID = 'session_id'

from threading import Thread
from time import sleep

class Session:

    confs = dict()
    impls = list()

    class CleaningThread(Thread):

        def __init__(self):
            super(Session.CleaningThread, self).__init__()
            self.daemon = True

        def run(self):
            while True:
                for impl in Session.impls:
                    impl['cleaning_func']()
                sleep(Session.confs.get('cleaning_interval', 1))

    @staticmethod
    def registerImplement(cls, cleaning_func = None):
        Session.impls.append({'class':cls, 'cleaning_func':cleaning_func})


    def __init__(self, handler):
        self.handler = handler
        self.sid = self.getSid()
        if not self.isInPool():
            self.setSid(self.initNewSession())

    def __del__(self):
        self.refreshExpiryTime()

    def getSid(self):
        return self.handler.get_cookie(COOKIES_NAME_SESSION_ID)

    def setSid(self, sid):
        return self.handler.set_cookie(COOKIES_NAME_SESSION_ID, '%s' % sid)

    def __getitem__(self, value_name):
        raise NotImplementedError()

    def __setitem__(self, value_name, value_data):
        raise NotImplementedError()

    def initNewSession(self):
        raise NotImplementedError()

    def refreshExpiryTime(self):
        raise NotImplementedError()

    def isInPool(self):
        raise NotImplementedError()

Session.CleaningThread().start()
