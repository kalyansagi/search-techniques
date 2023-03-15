import random
import copy


class Puzzle(object):
    def __init__(self, start: object, end: object):
        """
        A constructor function to initialize the puzzle
        :param start: begin state of the puzzle
        :param end: end state of the puzzle
        """
        self.start = start
        self.end = end
        self.blankSpacePosition = []
        self.findBlankSpacePosition()

    def isGoalReached(self):
        """
        function to check if the start state of the puzzle is same as end state.
        :return: true
        """
        return self.start == self.end

    def findBlankSpacePosition(self):
        """
        function to find out where the blank or empty position is in the given puzzle.
        iterating through the rows and columns in a nested loop until the empty position is found.
        :return: position of the blank.
        """
        for i, row in enumerate(self.start):
            for j, column in enumerate(row):
                if column == 0:
                    self.blankSpacePosition = [i, j]
                    return [i, j]


class TreeNode:
    def __init__(self, value, parent=None, last=None):
        """
        A constructor function to initialize the nodes. i.e., various combinations of puzzles
        :param value: current node
        :param parent: parent node
        :param last: most recent move for the current node.
        children: collection holding all the children
        """
        self.value = value
        self.neighbors = []
        self.parent = parent
        self.blankSpacePosition = value.blankSpacePosition
        self.last = last

    def findNeighbors(self):
        """
        function to find all the neighbors (puzzles) and append to the collection.
        it is checking position of blank space and take directional movement.
        """
        """verify blank space to down is a valid and adding resulting puzzle neighbors list."""
        if (self.blankSpacePosition[0] < 2) and (self.last != "U"):
            self.neighbors.append(TreeNode(moveBlankSpace(self.value, "D"), self, "D"))
        """verify blank space to up is a valid and adding resulting puzzle neighbors list."""
        if (self.blankSpacePosition[0] > 0) and (self.last != "D"):
            self.neighbors.append(TreeNode(moveBlankSpace(self.value, "U"), self, "U"))
        """verify blank space to right is a valid and adding resulting puzzle neighbors list."""
        if (self.blankSpacePosition[1] < 2) and (self.last != "L"):
            self.neighbors.append(TreeNode(moveBlankSpace(self.value, "R"), self, "R"))
        """verify blank space to left is a valid and adding resulting puzzle neighbors list."""
        if (self.blankSpacePosition[1] > 0) and (self.last != "R"):
            self.neighbors.append(TreeNode(moveBlankSpace(self.value, "L"), self, "L"))


class BinaryTreeUtils:
    def bfs(self):
        """
        A function to iterate through all possible boards and categorizing them as explored/unexplored.
        Internally calling findNeighbors function in the conditional loop to explore all possible children/neighbor puzzle boards from current state.
        Every puzzle board is popped from the collection to verify if present state is the expected state. i.e., end
        Also, we are making sure same puzzle board is not verified more than once to avoid infinite loop.
        :return: puzzle. This can be either end state or None (if not found)
        """
        """This check if to verify if the state of the object is empty"""
        if not self:
            return None
        """Initializing the moves begin with 0"""
        moves = 0
        """A collection to hold the explored boards"""
        explored = []
        """starting with input object as unexplored state"""
        unexplored = [self]
        """A loop to explore all the possible nodes based on the blank space movements."""
        while unexplored:
            """Popping the first node from unexplored."""
            state = unexplored.pop(0)
            """verify if the current node is already the expected goal state. return if true"""
            if state.value.isGoalReached():
                return [state, moves]
            """verify if current node is already explored."""
            if explored.__contains__(state.value.start):
                continue
            """add current node to explored list"""
            explored.append(state.value.start)
            moves += 1
            """calling another function to find possible neighbors. i,e., different other boards with movements in blank space."""
            state.findNeighbors()
            """add all the neighbor boards to unexplored list to they can be verified"""
            unexplored.extend(state.neighbors)
        """final return if no goal state is found"""
        return [None, moves]


def moveBlankSpace(state, action) -> Puzzle:
    """
    A function to move the blank space across the board and create variants.
    :param state: object containing blank space position, start puzzle & end puzzle.
    :param action: U or D or L or R
    :return: puzzle
    """
    index = state.blankSpacePosition
    """Making a copy of original state to new object so original cannot be tampered."""
    new_puzzle = copy.deepcopy(state)
    """taking current board to perform the moves."""
    previous_puzzle = new_puzzle.start
    """blank space is moved based on the action sent. U/D/L/R"""
    if action == "U":
        position = previous_puzzle[index[0] - 1][index[1]]
        previous_puzzle[index[0]][index[1]] = position
        previous_puzzle[index[0] - 1][index[1]] = 0
    elif action == "D":
        position = previous_puzzle[index[0] + 1][index[1]]
        previous_puzzle[index[0]][index[1]] = position
        previous_puzzle[index[0] + 1][index[1]] = 0
    elif action == "L":
        position = previous_puzzle[index[0]][index[1] - 1]
        previous_puzzle[index[0]][index[1]] = position
        previous_puzzle[index[0]][index[1] - 1] = 0
    elif action == "R":
        position = previous_puzzle[index[0]][index[1] + 1]
        previous_puzzle[index[0]][index[1]] = position
        previous_puzzle[index[0]][index[1] + 1] = 0
        """calling findBlankSpacePosition to find the blank space position for the new board"""
    new_puzzle.findBlankSpacePosition()
    return new_puzzle


def tracing(child: TreeNode):
    """
    A function to navigate from child node to the parent with the entire navigation tree.
    :param child:
    :return: tree of nodes
    """
    nodes = []
    while child.parent:
        nodes.append(child)
        child = child.parent
    nodes.append(child)
    return nodes


def generateRandom() -> [[]]:
    """
    A function to be able to generate a random 8 puzzle board.
    :return: a random puzzle
    """
    utilized_values = []
    random_state = [[0] * 3 for _ in range(3)]
    for i, row in enumerate(random_state):
        for j, column in enumerate(row):
            k = random.choice([n for n in range(0, 9) if n not in utilized_values])
            utilized_values.append(k)
            random_state[i][j] = k
    return random_state


def printCurrentPuzzle(puzzle):
    """
    A function to iterate through rows followed by columns and print values in each cell of the puzzle.
    :param puzzle:
    """
    for row in puzzle:
        for column in row:
            print(column, end=" ")
        print("|")


def printFinalResult(puzzle):
    """
    A function to print the node attributes, including board.
    Internally iterating through the nodes, we call a utility function to trace from root to parent node.
    In addition to the board and move, we are also printing the cost of moves required to reach goal state.
    :param puzzle: goal state
    """
    if puzzle[0] is None:
        print("Not able to search")
        quit()
    last_node = puzzle[0]
    tree_nodes = tracing(last_node)
    moves: str = ""
    while tree_nodes:
        p = tree_nodes.pop()
        if p.last is not None:
            print("From here, move " + p.last + ": ")
            moves += p.last + " "
        print('-------')
        printCurrentPuzzle(p.value.start)
        print('-------')
        print()
    print('And thus we are finished, with path (' + moves.strip(' ') + ').')


utils = BinaryTreeUtils()
end = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]
# start = generateRandom()
start = [[1, 3, 4], [8, 0, 5], [7, 2, 6]]
# start = [[1, 3, 4], [8, 6, 2], [0, 7, 5]]

print("Current state:")
printCurrentPuzzle(start)
print("BFS search is in progress \n")

puzzle_board = Puzzle(start, end)
root = TreeNode(puzzle_board)
bfs_result = BinaryTreeUtils.bfs(root)
printFinalResult(bfs_result)
