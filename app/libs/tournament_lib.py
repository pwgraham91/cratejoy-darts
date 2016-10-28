import math
from random import shuffle

from app.models import Tournament, User, TournamentPlayer, Game


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
            seed=seed + 1
        )
        session.add(tournament_player)

    make_tournament_games(session, added_tournament.id)

    return added_tournament


def make_tournament_games(session, tournament_id):
    """ given a tournament, create games based on seeding """

    tournament_players = session.query(TournamentPlayer).filter(
        TournamentPlayer.tournament_id == tournament_id
    ).order_by(TournamentPlayer.seed).all()

    make_round_games(session, tournament_players, tournament_id)


def make_round_games(session, tournament_players, tournament_id):
    rounds_left = get_rounds_left(len(tournament_players))
    player_spots_in_round = 2 ** rounds_left
    num_games_in_round = player_spots_in_round / 2
    num_tournament_players = len(tournament_players)

    for i in range(num_games_in_round):
        # take the player at the index of where the game should be seeded. For example, in an 8-player round, in the
        # first game, it should be the #1 seed player vs the #8 seed player unless there are less than 8 players in
        # which case it is the #1 vs None
        player_2_index = player_spots_in_round - i
        if player_2_index > num_tournament_players:
            player_2 = None
        else:
            player_2 = tournament_players.pop().user

        game = Game(
            tournament_id=tournament_id,
            round=rounds_left,
            position=i,
            player_1=tournament_players.pop(0).user,
            player_2=player_2
        )
        session.add(game)


def get_rounds_left(tournament_players_count):
    """
        get number of rounds left given a count of players left in the tournament
        ex: 2 players -> 1
            3 players -> 2
            4 players -> 2
            5 players -> 3
            ... 20 -> 5
    """
    return int(math.ceil(math.log(tournament_players_count, 2)))
