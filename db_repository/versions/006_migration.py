from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('forfeit', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('round', SmallInteger),
    Column('tournament_id', Integer),
    Column('winner_id', BigInteger, nullable=False),
    Column('loser_id', BigInteger, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].columns['round'].create()
    post_meta.tables['game'].columns['tournament_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['game'].columns['round'].drop()
    post_meta.tables['game'].columns['tournament_id'].drop()
