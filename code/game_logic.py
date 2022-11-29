class GameLogic:
    print("Game Logic Object Created")

    # TODO add code here to manage the logic of your game
    turn = 0

    def checkTurn(self):
        if self.turn == 0:
            return 1
        elif self.turn % 2 == 0:
            # If self.turn is an even number then it is player two's turn
            return 2
        else:
            # If it is an odd number then it is player one's turn
            return 1


    def myFun(self):
        print("Hello People")
