from datetime import datetime
import sqlalchemy

from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False)
    avatar = db.Column(db.String(200))
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime)
    auto_sign_up = db.Column(db.Boolean, default=True, nullable=False)

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

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "admin": self.admin,
            "avatar": self.avatar,
            "active": self.active,
            "created_at": str(self.created_at),
        }


class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_started = db.Column(db.DateTime, nullable=False)
    random_draw = db.Column(db.Boolean, default=False, nullable=False)

    def __repr__(self):
        return 'id: {} random: {} date: {}'.format(self.id, self.random_draw,
                                                   datetime.strftime(self.date_started, '%m/%d/%Y'))


class TournamentPlayer(db.Model):
    """ through table to add players to tournament """
    id = db.Column(db.Integer, primary_key=True)
    seed = db.Column(db.SmallInteger)  # starts at 1

    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id', ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)

    tournament = db.relationship("Tournament", backref="tournament_players")
    user = db.relationship("User", backref="tournament_players")


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    forfeit = db.Column(db.Boolean, default=False, nullable=False)
    round = db.Column(db.SmallInteger)  # championship is round 1, semi-final is round 2
    position = db.Column(db.SmallInteger)  # starts at 0
    created_at = db.Column(db.DateTime)

    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'))
    winner_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    loser_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=False)
    player_1_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    player_2_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
    submitted_by_id = db.Column(db.BigInteger, db.ForeignKey('user.id', ondelete="CASCADE"))

    tournament = db.relationship("Tournament", backref="games")
    winner = db.relationship("User", foreign_keys=[winner_id], backref=sqlalchemy.orm.backref('winners'))
    loser = db.relationship("User", foreign_keys=[loser_id], backref=sqlalchemy.orm.backref('losers'))
    player_1 = db.relationship("User", foreign_keys=[player_1_id], backref=sqlalchemy.orm.backref('player_1s'))
    player_2 = db.relationship("User", foreign_keys=[player_2_id], backref=sqlalchemy.orm.backref('player_2s'))
    submitted_by = db.relationship("User", foreign_keys=[submitted_by_id], backref=sqlalchemy.orm.backref('submitters'))
