from app.models import Tournament


def make_tournament(session, date_started, random_draw, players):
    added_tournament = Tournament(
        date_started=date_started,
        random_draw=random_draw
    )
    session.add(added_tournament)

    # todo: add list of players

    return added_tournament
