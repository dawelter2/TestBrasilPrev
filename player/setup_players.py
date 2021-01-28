from player.player import Impulsive, Demanding, Cautious, Random


def setup_players():
    players = list()
    players.append(Impulsive())
    players.append(Demanding())
    players.append(Cautious())
    players.append(Random())
    return players
