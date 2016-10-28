def get_game_dict(game):
    game_dict = {
        'gameID': game.id,
        'player1': game_player_dict(game, True),
        'player2': game_player_dict(game, False),
    }
    return game_dict


def get_future_game_dict():
    fake_future_game = {
        'gameID': 'future',
        'player1': {
            'name': '',
            'id': 'future player 1'
        },
        'player2': {
            'name': '',
            'id': 'future player 2'
        }
    }
    return fake_future_game


def game_player_dict(game, player_1):
    """
    get customer player dict for the tournament representation
    :param game: Game
    :param player_1: boolean. True for player_1 in Game False for player_2
    """

    player = game.player_1 if player_1 else game.player_2

    player_dict = {
        'name': player.name if player else 'BYE',
        'id': player.id if player else 'BYE',
    }

    if player and game.winner_id == player.id:
        player_dict['winner'] = True

    return player_dict


def get_games_by_round(tournament_games):
    """ get array of rounds which contains arrays of games """
    round_games = []
    games_by_round = []
    current_round = tournament_games[0].round
    for game in tournament_games:
        if game.round == current_round:
            # make custom dict for this
            round_games.append(get_game_dict(game))
        else:
            games_by_round.append(round_games)
    # don't forget to put the last round in the games_by_round
    games_by_round.append(round_games)

    # if current round is not the championship round, fill in the rest of the future games
    add_future_games_to_games_by_round(games_by_round, current_round)

    return games_by_round


def add_future_games_to_games_by_round(games_by_round, current_round):
    if current_round > 1:
        current_round -= 1

        num_players_in_round = 2 ** current_round
        num_games = num_players_in_round / 2

        round_games = []

        for i in range(num_games):
            round_games.append(get_future_game_dict())

        games_by_round.append(round_games)

        add_future_games_to_games_by_round(games_by_round, current_round)
