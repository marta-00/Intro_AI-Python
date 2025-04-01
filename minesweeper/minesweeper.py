import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            # If the number of mines == number of cells, all are mines
            return self.cells
        return set()
        
    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            # If the number of mines == 0, all are safe
            return self.cells
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # Remove the cell from the sentence
            self.cells.remove(cell)
            # Decrease the count of mines
            self.count -= 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            # Remove the cell from the sentence
            self.cells.remove(cell)
            # Do not modify self.count, as it represents the number of mines


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        # Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # Mark the cell as safe
        self.mark_safe(cell)

        # Identify neighbors of the cell
        neighbors = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Skip the cell itself
                if (i, j) == cell:
                    continue
                # Add neighbors that are within bounds
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbors.add((i, j))

        # Exclude neighbors that are already known to be safe or mines
        undetermined_neighbors = neighbors - self.safes - self.mines

        # Add a new sentence to the knowledge base
        new_sentence = Sentence(undetermined_neighbors, count)
        self.knowledge.append(new_sentence)

        # Mark additional cells as safe or as mines
        updated = True
        while updated:
            updated = False
            sentences_to_remove = []  # Collect sentences to remove
            cells_to_mark_safe = set()  # Collect cells to mark as safe
            cells_to_mark_mine = set()  # Collect cells to mark as mines

            for sentence in self.knowledge[:]:  # Iterate over a copy of the list
                # Collect known mines
                cells_to_mark_mine.update(sentence.known_mines())

                # Collect known safes
                cells_to_mark_safe.update(sentence.known_safes())

                # Collect empty sentences to remove
                if not sentence.cells:
                    sentences_to_remove.append(sentence)

            # Mark all collected cells as mines
            for cell in cells_to_mark_mine:
                if cell not in self.mines:
                    self.mark_mine(cell)
                    updated = True

            # Mark all collected cells as safe
            for cell in cells_to_mark_safe:
                if cell not in self.safes:
                    self.mark_safe(cell)
                    updated = True

            # Remove empty sentences after iteration
            for sentence in sentences_to_remove:
                self.knowledge.remove(sentence)

        # Infer new sentences from existing knowledge
        inferred_sentences = []
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 != sentence2 and sentence1.cells.issubset(sentence2.cells):
                    # Infer a new sentence
                    inferred_cells = sentence2.cells - sentence1.cells
                    inferred_count = sentence2.count - sentence1.count
                    new_sentence = Sentence(inferred_cells, inferred_count)

                    # Add the new sentence if it's not already in the knowledge base
                    if new_sentence not in self.knowledge and new_sentence not in inferred_sentences:
                        inferred_sentences.append(new_sentence)

        # Add all inferred sentences to the knowledge base
        self.knowledge.extend(inferred_sentences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Iterate through all known safe cells
        for cell in self.safes:
            # Return the first safe cell that has not been chosen yet
            if cell not in self.moves_made:
                return cell

        # If no safe move is available, return None
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Generate all possible cells on the board
        all_cells = set(itertools.product(range(self.height), range(self.width)))

        # Exclude cells that have already been chosen or are known to be mines
        possible_moves = all_cells - self.moves_made - self.mines

        # If there are no possible moves, return None
        if not possible_moves:
            return None

        # Choose a random move from the remaining possible moves
        return random.choice(list(possible_moves))
