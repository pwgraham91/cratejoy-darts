from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
tournament_player = Table('tournament_player', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('seed', SmallInteger),
    Column('tournament_id', Integer, nullable=False),
    Column('user_id', BigInteger, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tournament_player'].columns['seed'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['tournament_player'].columns['seed'].drop()
