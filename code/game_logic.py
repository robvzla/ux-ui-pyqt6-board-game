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


def checkTopLeftCorner(count, array, x, y, z):
    if checkBottom(array, x, y) == z:
        count += count
    if checkBottomRight(array, x, y) == z:
        count += count
    if checkRight(array, x, y) == z:
        count += count
    return count


def checkTopRightCorner(count, array, x, y, z):
    if checkLeft(array, x, y) == z:
        count += count
    if checkBottomLeft(array, x, y) == z:
        count += count
    if checkBottom(array, x, y) == z:
        count += count
    return count


def checkTopRow(count, array, x, y, z):
    if checkLeft(array, x, y) == z:
        count += count
    if checkBottomLeft(array, x, y) == z:
        count += count
    if checkBottom(array, x, y) == z:
        count += count
    if checkBottomRight(array, x, y) == z:
        count += count
    if checkRight(array, x, y) == z:
        count += count
    return count

def checkBottomLeftCorner(count, array, x, y, z):
    if y == 0:
        if checkTop(array, x, y) == z:
            count += count
        if checkTopRight(array, x, y) == z:
            count += count
        if checkRight(array, x, y) == z:
            count += count
        return count


def checkBottomRightCorner(count, array, x, y, z):
    if checkLeft(array, x, y) == z:
        count += count
    if checkTopLeft(array, x, y) == z:
        count += count
    if checkTop(array, x, y) == z:
        count += count
    return count


def checkBottomRow(count, array, x, y, z):
    if checkLeft(array, x, y) == z:
        count += count
    if checkTopLeft(array, x, y) == z:
        count += count
    if checkTop(array, x, y) == z:
        count += count
    if checkTopRight(array, x, y) == z:
        count += count
    if checkRight(array, x, y) == z:
        count += count
    return count


def checkLeftColumn(count, array, x, y, z):
    if checkTop(array, x, y) == z:
        count += count
    if checkTopRight(array, x, y) == z:
        count += count
    if checkRight(array, x, y) == z:
        count += count
    if checkBottomRight(array, x, y) == z:
        count += count
    if checkBottom(array, x, y) == z:
        count += count
    return count


def checkRightColumn(count, array, x, y, z):
    if checkTop(array, x, y) == z:
        count += count
    if checkTopLeft(array, x, y) == z:
        count += count
    if checkLeft(array, x, y) == z:
        count += count
    if checkBottomLeft(array, x, y) == z:
        count += count
    if checkBottom(array, x, y) == z:
        count += count
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
        count = 0

        # Search the intersections surrounding the intersection in question
        # Check the top left and right corners & the top row
        if x == 0:
            # Check top left corner
            if y == 0:
                return checkTopLeftCorner(count, array, x, y, z)
            # Check top right corner
            elif y == len(array):
                return checkTopRightCorner(count, array, x, y, z)
            # Check the top row
            else:
                return checkTopRow(count, array, x, y, z)

        # Check the bottom corners and the bottom row
        elif x == len(array):
            # Check the bottom left corner
            if y == 0:
                return checkBottomLeftCorner(count, array, x, y, z)
            # Check the bottom right corner
            elif y == len(array):
                return checkBottomRightCorner(count, array, x, y, z)
            # Check the bottom row
            else:
                return checkBottomRow(count, array, x, y, z)
        # Check the left column
        elif y == 0:
            if 0 < x < len(array):
                return checkLeftColumn(count, array, x, y, z)
        # Check the right column
        elif y == len(array):
            if 0 < x < len(array):
                return checkRightColumn(count, array, x, y, z)
        # Check everywhere else
        else:
            count = checkBottomRow(count, array, x, y, z)
            if checkBottomLeft(array, x, y) == z:
                count += count
            if checkBottom(array, x, y) == z:
                count += count
            if checkBottomRight(array, x, y) == z:
                count += count
            return count


