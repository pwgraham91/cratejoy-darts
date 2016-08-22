from app import db
import sqlalchemy


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_started = db.Column(db.DateTime, default=sqlalchemy.func.now())


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forfeit = db.Column(db.Boolean, default=False, nullable=False)
    round = db.Column(db.SmallInteger)

    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    winner_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    loser_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    tournament = db.relationship("Tournament", backref="games")
    winner = db.relationship("User", foreign_keys=[winner_id], backref=sqlalchemy.orm.backref('winners'))
    loser = db.relationship("User", foreign_keys=[loser_id], backref=sqlalchemy.orm.backref('losers'))
