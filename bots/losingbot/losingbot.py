from api import Deck

class Bot:
	def __init__(self):
		pass

	def get_move(self, state):
		moves = state.moves()
		moves = [move for move in moves if move[0] is not None and move[1] is None]

		# get trump moves
		moves_trump_suit = [move for move in moves if Deck.get_suit(move[0]) == state.get_trump_suit()]

		moves_not_trump = []
		if len(moves_trump_suit) > 0:
			moves_not_trump = [(move, move[0] % 5) for move in moves if move not in moves_trump_suit]
		else:
			moves_not_trump = [(move, move[0] % 5) for move in moves]
		moves_not_trump = self.sort_list(moves_not_trump)

		# play lower than opponent, otherwise fall back to lowest
		opponent_card = state.get_opponents_played_card()
		if opponent_card is not None:
			moves_same_suit = [move for move in moves if Deck.get_suit(move[0]) == Deck.get_suit(opponent_card)]
			move_set = [(move, move[0] % 5) for move in moves_same_suit]
			move_set = [move for move in move_set if move[1] > opponent_card % 5]
			move_set = self.sort_list(move_set)
			if len(move_set) > 0:
				return move_set[-1][0]

		if len(moves_not_trump) > 0:
			return moves_not_trump[-1][0]
		else:
			move_set = [(move, move[0] % 5) for move in moves]
			move_set = self.sort_list(move_set)
			return move_set[-1][0]

	def sort_list(self, sub_list): 
		return sorted(sub_list, key = lambda x: x[1])
