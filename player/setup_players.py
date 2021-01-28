from player.player import Impulsive, Demanding, Cautious, Random


def setup_players():
    impulsive = Impulsive()
    demanding = Demanding()
    cautious = Cautious()
    random = Random()
    return impulsive, demanding, cautious, random
