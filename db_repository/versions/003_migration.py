from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
game = Table('game', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('player_1_id', BIGINT),
    Column('player_2_id', BIGINT),
    Column('winner_id', BIGINT),
)

game = Table('game', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('winner_id', BigInteger),
    Column('loser_id', BigInteger),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['game'].columns['player_1_id'].drop()
    pre_meta.tables['game'].columns['player_2_id'].drop()
    post_meta.tables['game'].columns['loser_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['game'].columns['player_1_id'].create()
    pre_meta.tables['game'].columns['player_2_id'].create()
    post_meta.tables['game'].columns['loser_id'].drop()
