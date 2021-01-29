from play import Play, ROUNDS_LIMIT_REACHED, NORMAL_ENDING, ROUNDS_LIMIT
import pytest


def test_play(mocker):
    mocker.patch("play.roll_dice", return_value=6)

    # setup the game
    play = Play()
    player_impulsive = play.player_impulsive
    player_demanding = play.player_demanding
    player_cautious = play.player_cautious
    player_random = play.player_random

    # Validate if get_property_index return the right index
    assert player_impulsive.money == 300
    player_impulsive.last_property_landed = 4
    assert play.get_property_index(player_impulsive) == 10
    assert player_impulsive.money == 300

    # Validate if money is added to player every time he return to init of the board.
    player_impulsive.last_property_landed = 14
    assert play.get_property_index(player_impulsive) == 0
    assert player_impulsive.money == 400

    player_impulsive.last_property_landed = 18
    assert play.get_property_index(player_impulsive) == 4
    assert player_impulsive.money == 500

    # Validate if player will buy property and it will deduct from player's money
    player_impulsive.last_property_landed = 2
    assert player_impulsive.properties == []
    play.play_turn(player_impulsive)
    # validate if player is the owner
    assert play.properties[8].owner == player_impulsive
    assert player_impulsive.money == 300
    assert player_impulsive.properties == [play.properties[8]]

    # Validate if player is paying fee
    player_cautious.last_property_landed = 2
    assert player_cautious.money == 300
    play.play_turn(player_cautious)
    assert player_cautious.money == 260

    # Validate if a player is declared winner only with one active player left.
    assert play.check_victory() is None
    player_impulsive.money = -10
    player_random.money = -10
    assert play.check_victory() is None
    player_demanding.money = -10
    assert play.check_victory() == player_cautious

    # validate if the winner is the one with the highest amount of money, and if tie, the order is used as tiebreaker
    player_cautious.money = 750
    player_impulsive.money = 600
    player_random.money = 600
    player_demanding.money = 500
    assert play.find_winner() == player_cautious
    player_impulsive.money = 750
    assert play.find_winner() == player_impulsive


@pytest.mark.parametrize("dice_result, expect_winner, expect_ending_type", [
    (1, "Demanding", ROUNDS_LIMIT_REACHED),
    (2, "Demanding", ROUNDS_LIMIT_REACHED),
    (3, "Demanding", ROUNDS_LIMIT_REACHED),
    (4, "Impulsive", ROUNDS_LIMIT_REACHED),
    (5, "Impulsive", ROUNDS_LIMIT_REACHED),
    (6, "Demanding", ROUNDS_LIMIT_REACHED),
])
def test_play_game(mocker, dice_result, expect_winner, expect_ending_type):
    import play as p
    p.ROUNDS_LIMIT = 10
    mocker.patch("play.roll_dice", return_value=dice_result)
    mocker.patch("player.player.randint", return_value=1)

    play = Play()
    play.player_impulsive.money = 200
    play.player_demanding.money = 200
    play.player_cautious.money = 200
    play.player_random.money = 200

    # Play a 10 turn game
    winner, ending_type = play.play()
    assert type(winner).__name__ == expect_winner
    assert ending_type == expect_ending_type
