import random
from collections import defaultdict
import operator
# blah
ops = { "+": operator.add, "-": operator.sub }

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
			self.discard[card.value] +=1
			self.count += 1
			return card
		return self.draw_card()	


class PlayerCard:

	valence = ("+", "-")
	
	def __init__(self):
		self.value = random.randint(1,6)
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

	def get_side_deck(self):

		self.side = SideDeck(self.name)

		print(f"Choose your hand")

		for i in range(4):
			print(f"\n{self.side.name}:")
			counter = 1
			for card in self.side.cards:
				print(f"{counter}: {card.valence}{card.value}")
				counter += 1
			# print(list(enumerate(self.side.cards)))
			choice = int(input(f"\nChoose by number: "))
			self.side.choose_card(choice)
			print(f"\n\n\n{self.name}'s hand ({i+1}/4): \n"
				f"{self.side.hand}")





def draw_phase(player):
	print(f"{player.name} draws...\n")
	draw = maindeck.draw_card()
	print(draw.value)
	player.total += draw.value
	print(f"\n{player.name}'s current total is {player.total}\n")


def play_phase(player):
	played = False
	while played == False:
		print("1: Play card    2: Hit    3: Stay")
		action = input("Choose an action: ")
		action = action.strip()
		if action not in ["1", "2", "3"]:
			print("I'm sorry, I didn't understand that.\n"
				"Please enter 1, 2, or 3. ")
		if action == "1":
			played = True
			return "card"
		if action == "2":
			played = True
			return "hit"
		if action == "3":
			played = True
			return "stay"

def empty_hand(player):
	played = False
	while played == False:
		print("1: Hit    2: Stay")
		action = input("Choose an action: ")
		action = action.strip()
		if action not in ["1", "2"]:
			print("I'm sorry, I didn't understand that.\n"
				"Please enter 1 or 2.")
		if action == "1":
			played = True
			return "hit"
		if action == "2":
			played = True
			return "stay"



def play_card(player):
	while True:
		print(f"{player.name}'s hand:\n")

		for i in range(1, len(player.side.hand)+1):
			print(f"{i}: {player.side.hand[i-1]}")

		try:
			choice = player.side.hand.pop(int(input("Please enter a number: "))-1)
			break
		except (ValueError, IndexError):
			print("I'm sorry, I didn't understand that.\n"
				"Please enter a valid number.\n")
	player.total = ops[choice.valence](player.total,choice.value)
	print(f"\n{player.name}'s new total is {player.total}\n")



def round(player1, player2):
	players = [player1, player2]
	first = players.pop(random.randint(0,1))
	second = players[0]
	print(f"{first.name} goes first!")








# testing
player =  Player("player")
maindeck = MainDeck()


player.get_side_deck()
draw_phase(player)

play_card(player)