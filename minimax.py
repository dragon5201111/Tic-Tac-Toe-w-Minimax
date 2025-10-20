import math
import random

class Board:
    BLANK_SLOT = ' '
    def __init__(self, minPlayer, maxPlayer):
        self.minPlayer = minPlayer
        self.maxPlayer = maxPlayer
        self.board = [[Board.BLANK_SLOT for _ in range(3)] for _ in range(3)]

    def __str__(self):
        boardStr = ""
        for row in range(3):
            boardStr += "-" * 7 + "\n"
            boardStr += f"|{self.board[row][0]}|{self.board[row][1]}|{self.board[row][2]}|\n"
        boardStr += "-" * 7 + "\n"
        return boardStr


    def clone(self):
        newBoard = Board(self.minPlayer, self.maxPlayer)
        newBoard.board = [row[:] for row in self.board]
        return newBoard

    def isTie(self):
        for row in range(3):
            for column in range(3):
                if self.board[row][column] == Board.BLANK_SLOT:
                    return False
        return (not self.playerWon(self.maxPlayer)) and (not self.playerWon(self.minPlayer))

    def playerWon(self, player):
        return (self.board[0][0] == player and self.board[0][1] == player and self.board[0][2] == player) or\
               (self.board[1][0] == player and self.board[1][1] == player and self.board[1][2] == player) or\
               (self.board[2][0] == player and self.board[2][1] == player and self.board[2][2] == player) or\
               (self.board[0][0] == player and self.board[1][0] == player and self.board[2][0] == player) or\
               (self.board[0][1] == player and self.board[1][1] == player and self.board[2][1] == player) or\
               (self.board[0][2] == player and self.board[1][2] == player and self.board[2][2] == player) or\
               (self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player) or\
               (self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player)

    def value(self):
        if self.playerWon(self.minPlayer):
            return -1
        elif self.playerWon(self.maxPlayer):
            return 1
        return 0

    def isTerminal(self):
        return self.playerWon(self.minPlayer) or self.playerWon(self.maxPlayer) or self.isTie()

    def winner(self):
        if self.playerWon(self.minPlayer):
            return self.minPlayer
        elif self.playerWon(self.maxPlayer):
            return self.maxPlayer
        elif self.isTie():
            return "Tie"
        return ""

    # Returns all available actions from board state
    def actions(self):
        actions = []
        for row in range(3):
            for column in range(3):
                if self.board[row][column] == Board.BLANK_SLOT:
                    actions.append((row, column))
        return actions

    # Applies an action to a new board, returning a new cloned Board object
    def result(self, action : (int, int), player : str):
        newBoard = self.clone()
        row, column = action
        newBoard.board[row][column] = player
        return newBoard

    # Apply action to current board
    def applyAction(self, action : (int, int), player : str):
        (row, column) = action
        self.board[row][column] = player

    def maximize(self, alpha = -math.inf, beta = math.inf):
        if self.isTerminal():
            return self.value()

        value = -math.inf
        for action in self.actions():
            value = max(value, self.result(action, self.maxPlayer).minimize(alpha, beta))
            if value >= beta:
                return value
            alpha = max(alpha, value)
        return value

    def minimize(self, alpha = -math.inf, beta = math.inf):
        if self.isTerminal():
            return self.value()

        value = math.inf
        for action in self.actions():
            value = min(value, self.result(action, self.minPlayer).maximize(alpha, beta))
            if value <= alpha:
                return value
            beta = min(beta, value)
        return value

    def getBestMove(self, player):
        bestAction = ()
        bestActions = []
        bestValue = -math.inf

        for action in self.actions():
            nextValue = self.result(action, player).minimize()
            if nextValue > bestValue:
                bestValue = nextValue
                bestAction = action

                bestActions.clear()
                bestActions.append(action)

            elif nextValue == bestValue:
                bestActions.append(action)

        # If multiple best choices, select one at random
        if len(bestActions) > 1:
            return random.choice(bestActions)

        return bestAction

    def applyInput(self, _):
        try:
            row = int(input("Enter a row [0-2]: "))
            column = int(input("Enter a column [0-2]: "))
            if row < 0 or column < 0 or self.board[row][column] != Board.BLANK_SLOT:
                raise Exception("")
            print()
            return row, column
        except Exception as _:
            print("Invalid row, column pair entered.")
            return self.applyInput(_)


if __name__ == "__main__":
    players = {
        0 : "O",
        1 : "X"
    }

    currentPlayer = 0
    # maxPlayer is the AI agent
    board = Board(minPlayer=players[0], maxPlayer=(players[1]))

    actions = {
        0 : board.applyInput,
        1 : board.getBestMove
    }

    while not board.isTerminal():
        print(board)

        if players[currentPlayer] == board.maxPlayer:
            print("AI turn...")

        action = actions[currentPlayer](players[currentPlayer])
        board.applyAction(action, players[currentPlayer])
        # 0 ^ 1 = 1, 1 ^ 1 = 0
        currentPlayer ^= 1

    print(board)
    print("Game over.")
    print(f"Winner: {board.winner()}.")




