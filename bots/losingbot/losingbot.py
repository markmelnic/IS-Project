from api import State
from api import Deck

class Bot:
	def __init__(self):
		pass

	def get_move(self, state):
		moves = state.moves()

		# get trump moves
		moves_trump_suit = [move for move in moves if move[0] is not None and Deck.get_suit(move[0]) == state.get_trump_suit()]

		moves_not_trump = []
		if len(moves_trump_suit) > 0:
			moves_not_trump = [(move, move[0] % 5) for move in moves if move not in moves_trump_suit and move[0] is not None]
			moves_not_trump = self.sort_list(moves_not_trump)
		else:
			moves_not_trump = moves

		# print(len(moves), moves)
		# print(len(moves_not_trump), moves_not_trump)
		# print(len(moves_trump_suit), moves_trump_suit)

		# play lower than opponent, otherwise fall back to lowest
		opponent_card = state.get_opponents_played_card()
		if opponent_card is not None:
			moves_same_suit = [move for move in moves if move[0] is not None and Deck.get_suit(move[0]) == Deck.get_suit(state.get_opponents_played_card())]
			move_set = [(move, move[0] % 5) for move in moves_same_suit if move[0] is not None]
			move_set = [move for move in move_set if move[1] > opponent_card % 5]
			move_set = self.sort_list(move_set)
			if len(move_set) > 0 and move_set[-1][0] is not None:
				return move_set[-1][0]

		if len(moves_not_trump) > 0 and moves_not_trump[0][0] is not None:
			if len(moves_not_trump[0]) == 2:
				return moves_not_trump[0][0]
			else:
				return moves_not_trump[0]
		else:
			move_set = [(move, move[0] % 5) for move in moves if move[0] is not None]
			move_set = self.sort_list(move_set)
			return move_set[0][0]

	def sort_list(self, sub_list): 
		return(sorted(sub_list, key = lambda x: x[1])) 
