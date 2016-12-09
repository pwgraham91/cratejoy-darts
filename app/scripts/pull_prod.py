import json
import requests
import sqlalchemy as sqla
from sqlalchemy import orm

import config
from app.models import User


def pull_user_data(session):
    print 'pulling users'
    user_data = requests.get(u"{}{}".format('https://www.cratejoydarts.pw/', 'export/users'))
    loaded_data = json.loads(user_data.text)
    for user_dict in loaded_data:
        if session.query(User).filter(User.email == user_dict['email']).count() == 0:
            user = User(
                name=user_dict['name'],
                email=user_dict['email'],
                avatar=user_dict['avatar'],
                active=True,
                created_at=user_dict['created_at'],
            )
            session.add(user)
    session.commit()
    print 'done pulling users'


if __name__ == '__main__':
    engine = sqla.create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)
    Session = orm.sessionmaker(bind=engine)
    session = Session()

    pull_user_data(session)
    print 'all done'
