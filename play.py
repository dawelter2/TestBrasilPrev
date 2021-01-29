import random
from typing import List, Optional, Tuple

from board_game.property import Property
from board_game.setup_game import setup_game
from player.player import Player
from player.setup_players import setup_players

ROUNDS_LIMIT_REACHED = "ROUNDS_LIMIT_REACHED"
NORMAL_ENDING = "NORMAL_ENDING"
ROUNDS_LIMIT = 1000


def roll_dice(sides=6) -> int:
    """
    Simulate the roll of a dice and return its value.
    """
    return random.randint(1, sides)


class Play:
    def __init__(self):
        self.properties: List[Property] = setup_game()
        self.player_impulsive, self.player_demanding, self.player_cautious, self.player_random = setup_players()
        self.all_players = [self.player_impulsive, self.player_demanding, self.player_cautious, self.player_random]

    def get_property_index(self, player: Player):
        """
        Based on player last property landed and the result of dice, calculate where the player will be in the board.
        :param player: The player which is playing this turn.
        :return: A index in the properties list
        """
        result = roll_dice()
        if player.last_property_landed + result >= len(self.properties):
            player.new_round()
            return player.last_property_landed + result - len(self.properties)
        else:
            return player.last_property_landed + result

    def play_turn(self, player: Player):
        """
        Play a turn in the game, with the following steps:
        * roll the dice and go the property
        * check if landed property has an owner or not
        * if property has a owner, pay the fee or if has not, decide if want to buy the property.
        * if paid the fee, check if player still in the game, otherwise return his properties to the game.
        :param player: The player to play this turn.
        """
        property_index = self.get_property_index(player)
        landed_property = self.properties[property_index]
        if landed_property.is_available_for_sale:
            if player.should_buy_property(landed_property.sell_value, landed_property.fee_value):
                player.money -= landed_property.sell_value
                player.properties.append(landed_property)
                landed_property.owner = player
        else:
            player.money -= landed_property.fee_value
            landed_property.owner.money += landed_property.fee_value
            if not player.is_alive:
                for property_owned in player.properties:
                    property_owned.owner = None
        player.last_property_landed = property_index
        player.round_counter += 1

    def check_victory(self) -> Optional[Player]:
        """
        Check if there is only 1 active player left, if so, return him as winner.
        :return: None if there is no winner, otherwise a Player
        """
        active_players = list()
        if self.player_impulsive.is_alive:
            active_players.append(self.player_impulsive)
        if self.player_demanding.is_alive:
            active_players.append(self.player_demanding)
        if self.player_cautious.is_alive:
            active_players.append(self.player_cautious)
        if self.player_random.is_alive:
            active_players.append(self.player_random)

        if len(active_players) <= 1:
            self.all_players.sort(key=lambda x: x.money, reverse=True)
            return self.all_players[0]

    def find_winner(self) -> Player:
        """
        Find the player with the highest amount of money, the play order is used as a tiebreaker.
        :return:
        """
        winner = self.player_impulsive
        if self.player_demanding.money > winner.money:
            winner = self.player_demanding
        if self.player_cautious.money > winner.money:
            winner = self.player_cautious
        if self.player_random.money > winner.money:
            winner = self.player_random
        return winner

    def play(self) -> Tuple[Player, str]:
        """
        Play the game for 1000 rounds, if no winner is declared before reaching 1000 rounds, the player with the highest
        amount of money is declared winner.
        :return:
        """
        for game_round in range(ROUNDS_LIMIT):
            if self.player_impulsive.is_alive:
                self.play_turn(self.player_impulsive)
            if self.player_demanding.is_alive:
                self.play_turn(self.player_demanding)
            if self.player_cautious.is_alive:
                self.play_turn(self.player_cautious)
            if self.player_random.is_alive:
                self.play_turn(self.player_random)
            victory = self.check_victory()
            if victory:
                return victory, NORMAL_ENDING
        else:
            return self.find_winner(), ROUNDS_LIMIT_REACHED


if __name__ == '__main__':
    rounds_limit_counter = 0
    rounds_average_counter = 0
    players_win_counter = {"Impulsive": 0, "Demanding": 0, "Cautious": 0, "Random": 0}

    for i in range(300):
        play = Play()
        player, ending_type = play.play()

        if ending_type == ROUNDS_LIMIT_REACHED:
            rounds_limit_counter += 1

        rounds_average_counter += player.round_counter
        players_win_counter[type(player).__name__] += 1

    greatest_player = sorted(players_win_counter.items(), key=lambda item: item[1], reverse=True)[0]

    print("Ended by rounds limit:", rounds_limit_counter)
    print("Rounds average:", rounds_average_counter / 300)
    print(f"Greatest player is {greatest_player[0]} with {greatest_player[1]} wins")
    print(f"Win rate for each player:")
    print(f"Impulsive: {round(players_win_counter['Impulsive'] / 300 * 100, 2)}%")
    print(f"Demanding: {round(players_win_counter['Demanding'] / 300 * 100, 2)}%")
    print(f"Cautious: {round(players_win_counter['Cautious'] / 300 * 100, 2)}%")
    print(f"Random: {round(players_win_counter['Random'] / 300 * 100, 2)}%")
