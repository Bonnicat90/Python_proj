def check_winner(board, mark):
    return (
        (board[7] == mark and board[8] == mark and board[9] == mark) or  # across the top
        (board[4] == mark and board[5] == mark and board[6] == mark) or  # across the middle
        (board[1] == mark and board[2] == mark and board[3] == mark) or  # across the bottom
        (board[7] == mark and board[4] == mark and board[1] == mark) or  # down the left side
        (board[8] == mark and board[5] == mark and board[2] == mark) or  # down the middle
        (board[9] == mark and board[6] == mark and board[3] == mark) or  # down the right side
        (board[7] == mark and board[5] == mark and board[3] == mark) or  # diagonal
        (board[9] == mark and board[5] == mark and board[1] == mark)     # diagonal
    )

def display_board(board):
    print('\n' + board[7] + '|' + board[8] + '|' + board[9])
    print('-----')
    print(board[4] + '|' + board[5] + '|' + board[6])
    print('-----')
    print(board[1] + '|' + board[2] + '|' + board[3] + '\n')


def play_game():
    board = [' '] * 10
    player1 = input("Please pick a marker 'X' or 'O': ").upper()
    player2 = 'O' if player1 == 'X' else 'X'
    
    numlist = list(range(1, 10))
    i = 1
    win = False
    
    while i <= 9 and not win:
        display_board(board)
        plyr1 = int(input(f'1st player, please pick a number among {numlist} to put your {player1} at step {i}: '))
        while plyr1 not in numlist:
            print(f'{plyr1} has been chosen, please re-select.')
            plyr1 = int(input(f'1st player, please pick a number among {numlist} to put your {player1} at step {i}: '))
        
        board[plyr1] = player1
        numlist.remove(plyr1)
        win = check_winner(board, player1)
        if win:
            print('Congrats! Player 1 wins!')
            display_board(board)
            return 'Player 1'
        
        i += 1
        if i > 9:
            break
        
        display_board(board)
        plyr2 = int(input(f'2nd player, please pick a number among {numlist} to put your {player2} at step {i}: '))
        while plyr2 not in numlist:
            print(f'{plyr2} has been chosen, please re-select.')
            plyr2 = int(input(f'2nd player, please pick a number among {numlist} to put your {player2} at step {i}: '))
        
        board[plyr2] = player2
        numlist.remove(plyr2)
        win = check_winner(board, player2)
        if win:
            print('Congrats! Player 2 wins!')
            display_board(board)
            return 'Player 2'
        
        i += 1
    
    display_board(board)
    print("It's a tie!")
    return 'Tie'

# Start the game
play_game()