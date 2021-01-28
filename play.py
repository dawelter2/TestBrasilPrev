import random
from typing import List, Optional

from board_game.property import Property
from board_game.setup_game import setup_game
from player.player import Player, RoundLimitExceeded
from player.setup_players import setup_players

ROUNDS_LIMIT = "ROUNDS_LIMIT"
NORMAL_ENDING = "NORMAL_ENDING"


def roll_dice(sides=6) -> int:
    return random.randint(0, sides - 1)


class Play:
    def __init__(self):
        self.properties: List[Property] = setup_game()
        self.player_impulsive, self.player_demanding, self.player_cautious, self.player_random = setup_players()
        self.all_players = [self.player_impulsive, self.player_demanding, self.player_cautious, self.player_random]

    def get_property_index(self, player):
        result = roll_dice()
        if player.last_property_landed + result >= len(self.properties):
            player.new_round()
            return player.last_property_landed + result - len(self.properties)
        else:
            return player.last_property_landed + result

    def play_turn(self, player: Player):
        property_index = self.get_property_index(player)
        landed_property = self.properties[property_index]
        if landed_property.owner is None:
            if player.should_buy_property(landed_property.get_sell_value(), landed_property.get_fee_value()):
                player.money -= landed_property.get_sell_value()
                player.properties.append(landed_property)
                landed_property.owner = player
        else:
            player.money -= landed_property.get_fee_value()
            landed_property.owner.money += landed_property.get_fee_value()
            if player.money < 0:
                for property_owned in player.properties:
                    property_owned.owner = None
        player.last_property_landed = property_index

    def check_victory(self) -> Optional[Player]:
        active_players = list()
        if self.player_impulsive.is_alive():
            active_players.append(self.player_impulsive)
        if self.player_demanding.is_alive():
            active_players.append(self.player_demanding)
        if self.player_cautious.is_alive():
            active_players.append(self.player_cautious)
        if self.player_random.is_alive():
            active_players.append(self.player_random)

        if len(active_players) <= 1:
            self.all_players.sort(key=lambda x: x.money, reverse=True)
            return self.all_players[0]

    def play(self):
        while True:
            try:
                if self.player_impulsive.is_alive():
                    self.play_turn(self.player_impulsive)
                if self.player_demanding.is_alive():
                    self.play_turn(self.player_demanding)
                if self.player_cautious.is_alive():
                    self.play_turn(self.player_cautious)
                if self.player_random.is_alive():
                    self.play_turn(self.player_random)
            except RoundLimitExceeded:
                self.all_players.sort(key=lambda x: x.money, reverse=True)
                return self.all_players[0], ROUNDS_LIMIT

            victory = self.check_victory()
            if victory:
                return victory, NORMAL_ENDING


if __name__ == '__main__':
    rounds_limit_counter = 0
    rounds_average_counter = 0
    players_win_counter = {"Impulsive": 0, "Demanding": 0, "Cautious": 0, "Random": 0}

    for i in range(300):
        play = Play()
        player, ending_type = play.play()

        if ending_type == ROUNDS_LIMIT:
            rounds_limit_counter += 1

        rounds_average_counter += player.round_count
        players_win_counter[type(player).__name__] += 1

    greatest_player = sorted(players_win_counter.items(), key=lambda item: item[1], reverse=True)[0]

    print("Ended by rounds limit:", rounds_limit_counter)
    print("Rounds average:", rounds_average_counter / 300)
    print(f"Greatest player is {greatest_player[0]} with {greatest_player[1]} wins")
    print(f"Win rate for each play)e:")
    print(f"Impulsive: {round(players_win_counter['Impulsive'] / 300 * 100, 2)}%")
    print(f"Demanding: {round(players_win_counter['Demanding'] / 300 * 100, 2)}%")
    print(f"Cautious: {round(players_win_counter['Cautious'] / 300 * 100, 2)}%")
    print(f"Random: {round(players_win_counter['Random'] / 300 * 100, 2)}%")
