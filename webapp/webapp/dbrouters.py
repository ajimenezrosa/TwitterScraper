from browse.models import Users

class UsersDBRouter(object):

    def db_for_read(self, model, **hints):
        if model == Users:
            return 'users'
        return None

    def db_for_write(self, model, **hints):
        if model == Users:
            return 'users'
        return None
