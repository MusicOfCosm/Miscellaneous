import itertools
import time

print("Tic-tac-toe")

def win(game):
    def same(liste):
        if liste.count(liste[0])==len(liste) and all(liste)==True:
            return True
        else:
            return False

    #This checks if you win with a honrizontal line
    for row in board:
        if same(row):
            print(f'Player {row[0]} wins with a horizontal line!')
            return True
    

    #This checks if you win with a vertical line
    for column in range(len(board)):
        vertical=[]

        for row in board:
            vertical.append(row[column])

        if same(vertical):
            print(f'Player {vertical[0]} wins with a vertical line!')
            return True
    

    #This checks if you win with a diagonal line
    diagonal1=[]
    diagonal2=[]

    for n in range(len(board)): #\
        diagonal1.append(board[n][n])

    for i, k in enumerate(reversed(range(len(board)))): #/
        diagonal2.append(board[i][k])
    
    if same(diagonal1):
        print(f'Player {diagonal1[0]} wins with a \\ diagonal line!')
        return True
    if same(diagonal2):
        print(f'Player {diagonal2[0]} wins with a / diagonal line!')
        return True

    return False

def tic_tac_toe(game_board, player=0, row=0, column=0, just_display=False):
    #this sets the default values of the parameters player, column, and row of tic_tac_toe() to 0
    
    try:
        if game_board[row][column]!=0:
            print('Choose coordinates that are not occupied!')
            return False

        if row<0:
            print('Please input correct values for the coordinates (A, B or C for column, and 1, 2 or 3 for row).')
            return False

        print("   A  B  C")
        
        if not just_display:
            game_board[row][column]=player
            #player is the number replacing what there is at the chosen coordinates
        
        for row_index, row in enumerate(game_board):
            print(row_index, row)
            #'row' are the rows of the board (obviously), 'row_index' are the numbers iterating every 'row'
        
        return game_board
    
    except:
        print('Please input correct values for the coordinates (A, B or C for column, and 1, 2 or 3 for row).')
        return False

    finally:
        print('')

play = True
players = [1,2]
while play:
    board = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
    game_won = False
    tic_tac_toe(board, just_display=True)
    player_cycle = itertools.cycle([1, 2]) #itertools.cycle makes it so that you can cycle between the last and the first values of an iterable
    while not game_won:
        current_player = next(player_cycle) #next just goes to the next value of a iterable (such as a list)
        print(f"Player: {current_player}")

        played = False
        while not played:
            try:
                column_letter = {'A' : 0, 'B' : 1, 'C' : 2}
                column_choice = int(column_letter[str(input("Which column (A, B, or C)? ").upper())])
                row_choice = int(input("Which row (0, 1, or 2)? "))
                game = tic_tac_toe(board, player=current_player, row=row_choice, column=column_choice)
            except:
                column_choice = 4
                row_choice = 0
                game = tic_tac_toe(board, player=current_player, row=row_choice, column=column_choice)

            if game: played = True

        if win(board):
            game_won = True
            play_again = input('Thank you for playing Tic-tac-toe! Would you like to play again? (y/n) ')
            if play_again.lower() == 'y' or play_again.lower() == 'yes': #string.lower() makes it that every letters are lowercase. There's also x.upper()
                print('\nBoard reset!')
                next

            elif play_again.lower() == 'n' or play_again.lower() == 'no':
                print('See you next time!')
                time.sleep(5)
                play = False

            else:
                print('Not a valid answer, closing the game...')
                time.sleep(5)
                play = False