board = [ " " for _ in range(9)]
def display_board():
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("--- | --- | ---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("--- | --- | ---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()
def check_winner(player):
    if ((board[0] == player and board[1] == player and board[2] == player) or (board[3] == player and board[4] == player and board[5] == player) or (board[6] == player and board[7] == player and board[8] == player)):
     return True
    if ((board[0] == player and board[3] == player and board[6] == player) or (board[1] == player and board[4] == player and board[7] == player) or (board[2] == player and board[5] == player and board[8] == player)):
     return True
    if ((board[0] == player and board[4] == player and board[8] == player) or (board[2] == player and board[4] == player and board[6] == player)):
        return True
    return False
def check_draw():
    return " " not in board
def player_move(player):
    while True:
        move = input(f"Joueur {player}, choisis une position (1 - 9) : ")
        if move.isdigit():
            move = int(move) - 1
            if 0 <= move <= 8:
                if board[move] == " ":
                    board[move] = player
                    break
                else:
                    print("Cette case est déjà occupée.")
            else:
                print("Entre un nombre valide.")
def play_game():
    current_player = "X"
    while True:
        display_board()
        if check_winner(current_player):
            display_board()
            print(f" Le joueur {current_player} a gagné !")
            break
        if check_draw():
            display_board ()
            print(" Match nul !")
            break
        if current_player == "X":
            current_player = "0"
        else:
            current_player = "X"
play_game()
            
    
    