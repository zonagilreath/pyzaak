import random
from collections import defaultdict
import operator
import time

ops = {"+": operator.add, "-": operator.sub}


class Card:

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return str(self.value)


class MainDeck:
    def __init__(self):
        self.discard = defaultdict(int)
        self.count = 0

    def draw_card(self):
        if self.count == 40:
            print("Reshuffling deck...")
            self.discard.clear()
        card = Card(random.randint(1, 10))
        if self.discard[card.value] < 4:
            self.discard[card.value] += 1
            self.count += 1
            return card
        return self.draw_card()


class PlayerCard:

    valence = ("+", "-")

    def __init__(self):
        self.value = random.randint(1, 6)
        self.valence = random.choice(PlayerCard.valence)

    def __repr__(self):
        return f"{self.valence}{self.value}"


class SideDeck:

    def __init__(self, name):
        self.name = f"{name}'s side deck"
        self.cards = [PlayerCard() for i in range(10)]
        self.hand = []

    def choose_card(self, choice):
        self.hand.append(self.cards.pop(choice - 1))


class Player:

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.total = 0
        self.standing = False
        self.bust = False

    def __repr__(self):
        return(f"Name: {self.name}, Score: {self.score},\n"
               f"Total: {self.total}, Standing: {self.standing},\n"
               f"Bust: {self.bust}")

    def get_side_deck(self):
        space()
        pause()
        self.side = SideDeck(self.name)

        print(f"{self.name}, choose your hand (0/4)")

        for i in range(4):
            print(f"\n{self.side.name}:")
            counter = 1
            for card in self.side.cards:
                print(f"{counter}: {card.valence}{card.value}")
                counter += 1
            # print(list(enumerate(self.side.cards)))
            choice = int(input(f"\nChoose by number: "))
            self.side.choose_card(choice)
            space()
            print(f"{self.name}'s hand ({i+1}/4): \n"
                  f"{self.side.hand}")

    def round_reset(self):
        self.total = 0
        self.bust = False
        self.standing = False

    def check_bust(self):
        if self.total > 20:
            self.bust = True
            self.total = -220
            print(self.name, "busts!")


def pause(sec=0.4):
    time.sleep(sec)


def space(size=20):
    for i in range(size):
        print("\n")


def continue_play(player):
    if not(player.bust or player.standing):
        return True
    return False


def stand(player):
    player.standing = True


def pass_turn(player):
    pass


def draw_phase(player, maindeck):
    print(f"{player.name} draws...\n")
    draw = maindeck.draw_card()
    print(draw.value)
    player.total += draw.value
    print(f"\n{player.name}'s current total is {player.total}\n")


def play_phase(player):
    actions = {"1": play_card,
               "2": pass_turn,
               "3": stand
               }
    show_hand(player)
    space(size=4)
    while True:
        print("Choose an action: ")
        print("1: Play card    2: Pass    3: Stand")

        try:
            actions[input("Selection: ")](player)
            break
        except KeyError:
            print("I'm sorry, I didn't understand that.\n"
                  "Please enter 1, 2, or 3.")


def play_phase_no_card(player):
    actions = {"1": pass_turn,
               "2": stand
               }
    while True:
        print("Choose an action: ")
        print("1: Pass    2: Stand")

        try:
            actions[input("Selection: ")](player)
            break
        except KeyError:
            print("I'm sorry, I didn't understand that.\n"
                  "Please enter 1 or 2.")


def show_hand(player):
    display = ""
    for i in player.side.hand:
        display += f"{i}   "
    print(f"{player.name}'s hand: ", display)


def show_hand_numbered(player):
    print(f"{player.name}'s hand:\n")
    for i in range(1, len(player.side.hand)+1):
        print(f"{i}: {player.side.hand[i-1]}")


def apply_card(player, choice):
    player.total = ops[choice.valence](player.total, choice.value)
    print(f"\n{player.name}'s new total is {player.total}\n")


def play_card(player):
    while True:

        show_hand_numbered(player)

        try:
            choice = player.side.hand.pop(
                int(input("Please enter a number: "))-1)
            break
        except (ValueError, IndexError):
            print("I'm sorry, I didn't understand that.\n"
                  "Please enter a valid number.\n")
    apply_card(player, choice)
    play_phase_no_card(player)


def player_turn(player, maindeck):
    space()
    pause()
    if continue_play(player):
        draw_phase(player, maindeck)
    if continue_play(player):
        play_phase(player) if player.side.hand else play_phase_no_card(player)
        player.check_bust()


def play_order(player1, player2):
    players = [player1, player2]
    first = players.pop(random.randint(0, 1))
    second = players[0]
    print(f"{first.name} goes first!")
    return first, second


def win_round(player1, player2):
    if player1.total == player2.total:
        print("No winner!")
    else:
        winner = max(player1, player2, key=operator.attrgetter('total'))
        print(f"{winner.name} wins the round!")
        winner.score += 1


def round(player1, player2, maindeck):
    player1.round_reset()
    player2.round_reset()
    first, second = play_order(player1, player2)
    while (continue_play(first) or continue_play(second)):
        player_turn(first, maindeck)
        player_turn(second, maindeck)
    space(size=4)
    win_round(player1, player2)
    pause(sec=2.5)


def score_to_win():
    while True:

        try:
            score_to_win = int(input("How many points to win?  ").strip())
            break
        except TypeError:
            print("I'm sorry, I didn't understand that.\n"
                  "Please enter a number.\n")
    return score_to_win


def get_players():
    player1 = Player(input("Player 1 name: "))
    pause()
    print(f"Hi, {player1.name}!")
    space(size=4)
    pause()
    player2 = Player(input("Player 2 name: "))
    pause()
    print(f"Hey, {player2.name}!")
    space(size=4)
    return player1, player2


def game(player1, player2, score_to_win, maindeck):
    player1.get_side_deck()
    player2.get_side_deck()
    while (player1.score < score_to_win) and (player2.score < score_to_win):
        round_count = 1
        print("Round", round_count)
        round(player1, player2, maindeck)
        round_count += 1
    winner = max(player1, player2, key=operator.attrgetter('score'))
    loser = min(player1, player2, key=operator.attrgetter('score'))
    print(f"{winner.name} wins the game!!!")
    pause()
    print(f"Congrats {winner.name}!")
    pause()
    print(f"Better luck next time {loser.name}...")
    pause(sec=4)


def __main__():
    space()
    player1, player2 = get_players()
    stw = score_to_win()
    maindeck = MainDeck()
    game(player1, player2, stw, maindeck)


# testing
# player1 = Player("player1")
# player2 = Player("player2")
# maindeck = MainDeck()


# player1.get_side_deck()
# show_hand(player1)
# player2.get_side_deck()

# round(player1, player2)


__main__()
