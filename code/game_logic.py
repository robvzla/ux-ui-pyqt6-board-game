# Methods to return what is surrounding the intersection
def checkLeft(array, x, y):
    return array[x][y - 1]


def checkTopLeft(array, x, y):
    return array[x - 1][y - 1]


def checkTop(array, x, y):
    return array[x - 1][y]


def checkTopRight(array, x, y):
    return array[x - 1][y + 1]


def checkRight(array, x, y):
    return array[x][y + 1]


def checkBottomRight(array, x, y):
    return array[x + 1][y + 1]


def checkBottom(array, x, y):
    return array[x + 1][y]


def checkBottomLeft(array, x, y):
    return array[x + 1][y - 1]


def checkTopLeftCorner(array, x, y, z):
    count = 0
    if checkBottom(array, x, y) == z:
        count += 1
    if checkBottomRight(array, x, y) == z:
        count += 1
    if checkRight(array, x, y) == z:
        count += 1
    return count


def checkTopRightCorner(array, x, y, z):
    count = 0
    if checkLeft(array, x, y) == z:
        print("Left: " + str(checkLeft(array, x, y)))
        count += 1
    if checkBottomLeft(array, x, y) == z:
        count += 1
    if checkBottom(array, x, y) == z:
        count += 1
    return count


def checkTopRow(array, x, y, z):
    count = checkTopRightCorner(array, x, y, z)
    if checkBottomRight(array, x, y) == z:
        count += 1
    if checkRight(array, x, y) == z:
        count += 1
    return count


def checkBottomLeftCorner(array, x, y, z):
    count = 0
    if y == 0:
        if checkTop(array, x, y) == z:
            count += 1
        if checkTopRight(array, x, y) == z:
            count += 1
        if checkRight(array, x, y) == z:
            count += 1
        return count


def checkBottomRightCorner(array, x, y, z):
    count = 0
    if checkLeft(array, x, y) == z:
        count += 1
    if checkTopLeft(array, x, y) == z:
        count += 1
    if checkTop(array, x, y) == z:
        count += 1
    return count


def checkBottomRow(array, x, y, z):
    count = checkBottomRightCorner(array, x, y, z)
    if checkTopRight(array, x, y) == z:
        count += 1
    if checkRight(array, x, y) == z:
        count += 1
    return count


def checkLeftColumn(array, x, y, z):
    count = 0
    if checkTop(array, x, y) == z:
        count += 1
    if checkTopRight(array, x, y) == z:
        count += 1
    if checkRight(array, x, y) == z:
        count += 1
    if checkBottomRight(array, x, y) == z:
        count += 1
    if checkBottom(array, x, y) == z:
        count += 1
    return count


def checkRightColumn(array, x, y, z):
    count = 0
    if checkTop(array, x, y) == z:
        count += 1
    if checkTopLeft(array, x, y) == z:
        count += 1
    if checkLeft(array, x, y) == z:
        count += 1
    if checkBottomLeft(array, x, y) == z:
        count += 1
    if checkBottom(array, x, y) == z:
        count += 1
    return count


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

    def checkAroundIntersection(self, x, y, array, z):
        # Search the intersections surrounding the intersection in question
        # Check the top left and right corners & the top row
        if x == 0:
            # Check top left corner
            if y == 0:
                return checkTopLeftCorner(array, x, y, z)  # Working correctly
            # Check top right corner
            elif y == (len(array) - 1):
                return checkTopRightCorner(array, x, y, z)  # Working correctly
            # Check the top row
            else:
                return checkTopRow(array, x, y, z)  # Working correctly

        # Check the bottom corners and the bottom row
        elif x == (len(array) - 1):
            # Check the bottom left corner
            if y == 0:
                return checkBottomLeftCorner(array, x, y, z)  # Working correctly
            # Check the bottom right corner
            elif y == (len(array) - 1):
                return checkBottomRightCorner(array, x, y, z)  # Working correctly
            # Check the bottom row
            else:
                return checkBottomRow(array, x, y, z)  # Working correctly
        # Check the left column
        elif y == 0:
            if 0 < x < (len(array) - 1):
                return checkLeftColumn(array, x, y, z)  # Working correctly
        # Check the right column
        elif y == (len(array) - 1):
            if 0 < x < (len(array) - 1):
                return checkRightColumn(array, x, y, z)  # Working correctly
        # Check everywhere else
        else:  # Working correctly
            count = checkBottomRow(array, x, y, z)
            if checkBottomLeft(array, x, y) == z:
                count += 1
            if checkBottom(array, x, y) == z:
                count += 1
            if checkBottomRight(array, x, y) == z:
                count += 1
            return count