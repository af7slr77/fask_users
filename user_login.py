from models import User


class UserLogin():
    def from_db(self, user_id, db):
        self.__user = db.one_or_404(db.select(User).filter_by(id=user_id))
        return self

    def crate(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__user.id)