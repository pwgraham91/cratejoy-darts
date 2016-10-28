from random import shuffle

from app.models import Tournament, User, TournamentPlayer


def make_tournament(session, date_started, random_draw, player_ids):
    added_tournament = Tournament(
        date_started=date_started,
        random_draw=random_draw
    )
    session.add(added_tournament)

    players = session.query(User).filter(
        User.id.in_([int(id) for id in player_ids])
    ).all()

    # randomize
    shuffle(players)

    for seed, player in enumerate(players):
        tournament_player = TournamentPlayer(
            user=player,
            tournament=added_tournament,
            seed=seed
        )
        session.add(tournament_player)

    return added_tournament
