from os import system


GREEN = '\u001b[32m'
RED = '\u001b[31m'
CYAN = '\u001b[36m'
BLACK = '\u001b[30;1m'
WHITE = '\u001b[37;1m'
BG_BLUE = '\u001b[44;1m'
BG_WHITE = '\u001b[47;1m'
BG_PINK = '\u001b[45m'
END = '\033[0m'


# This function prompts the player to choose a piece to move.
def choose_piece(position, available_pieces = None):
    while True:
        if available_pieces:
            print("You can only choose the highlighted pieces.")
        raw = input("Enter the piece coordinates: ")
        try:
            coordinates = (int(raw[0])), (ord(raw[1]) - 65)
            field = position.get_table()[coordinates[0]][coordinates[1]]
            if available_pieces:
                if coordinates in available_pieces:
                    if position.get_turn() and field.lower() == "x":
                        next_moves = position.find_valid_moves_for_piece(coordinates)
                        if len(next_moves) != 0:
                            return coordinates
                        else:
                            print("Chosen piece has no available moves!")
                            continue
                    elif not position.get_turn() and field.lower() == "o":
                        return coordinates
                    else:
                        print("Selection is not valid! Try again.")
            else:
                if position.get_turn() and field.lower() == "x":
                    next_moves = position.find_valid_moves_for_piece(coordinates)
                    if len(next_moves) != 0:
                        return coordinates
                    else:
                        print("Chosen piece has no available moves!")
                        continue
                elif not position.get_turn() and field.lower() == "o":
                    return coordinates
                else:
                    print("Selection is not valid! Try again.")
        except:
            print("Invalid coordinates! Try again.")


# This function prompts the player to choose a position to move to.
def choose_field(valid_moves):
    while True:
        raw = input(
            "Enter the field coordinates: ")
        try:
            coordinates = (int(raw[0])), (ord(raw[1]) - 65)
            if coordinates not in valid_moves:
                print("Selection is not valid! Try again.")
            else:
                return coordinates
        except:
            print("Invalid coordinates! Try again.")


# This function prints the table. It accepts two additional parameters, selected and valid_moves.
# If additional parameters are supplied, it will print the table with prompts for valid_moves or selected piece.
def print_table(table, selected = None, valid_moves = None):
    system('clear')
    for i in range(len(table)):
        if i == 0:
            print("    A    B    C    D    E    F    G    H")
            print("  __________________________________________")
        for j in range(len(table[i])):
            if j == 0:
                print(i, end=" |")
            if table[i][j] == "b" or table[i][j] == "B":
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(BG_BLUE + BLACK + " " +
                          str(table[i][j]) + " " + END, end="  ")
                else:
                    print(GREEN + " " +
                          str(table[i][j]) + " " + END, end="  ")
            elif table[i][j] == "c" or table[i][j] == "C":
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(BG_BLUE + BLACK + " " +
                          str(table[i][j]) + " " + END, end="  ")
                else:
                    print(RED + " " +
                          str(table[i][j]) + " " + END, end="  ")

            elif valid_moves and (i, j) in valid_moves:
                print(BG_WHITE + BLACK + str(i) +
                      " " + str(chr(j + 65)) + END, end="  ")
            else:
                if selected and ((i, j) in selected or (i, j) == selected):
                    print(BG_PINK + BLACK + " " +
                          str(table[i][j]) + " " + END, end="  ")
                else:
                    print(" " + str(table[i][j]) + " ", end="  ")
        print("| ")
    print("  ------------------------------------------")
