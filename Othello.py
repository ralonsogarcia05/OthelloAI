#Richard Alonso Garcia
#Introduction To Artifical Intelligence (Spring 2025)
# AI Othello Game 

#evaluates board using different variables,
def evaluateBoard(board, player):
    opponent = 1 - player
    my_discs = 0
    opp_discs = 0
    my_moves = len(getChildren(board, player))
    opp_moves = len(getChildren(board, opponent))
    corners = [(0, 0), (0, 7), (7, 0), (7, 7)]

    corner_score = 0
    edge_score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == player:
                my_discs += 1
                if (i, j) in corners:
                    corner_score += WEIGHTS['corner']
                elif i == 0 or i == 7 or j == 0 or j == 7:
                    edge_score += WEIGHTS['edge']
            elif board[i][j] == opponent:
                opp_discs += 1
                if (i, j) in corners:
                    corner_score -= WEIGHTS['corner']
                elif i == 0 or i == 7 or j == 0 or j == 7:
                    edge_score -= WEIGHTS['edge']

    parity = WEIGHTS['parity'] * (my_discs - opp_discs)
    mobility = WEIGHTS['mobility'] * (my_moves - opp_moves)
    return corner_score + edge_score + parity + mobility

def printer(board):
    # prints board on screen
    print("    A   B   C   D   E   F   G   H")
    for i in range(1,N+1):
        print(" ", "-"*33)
        print(i,"",end="|")
        for j in range(0,N):
            if (board[i-1][j] == 0):
                print("","X","", end="|")    
            elif (board[i-1][j] == 1):
                print("","O","",end="|")
            else :
                print(""," ","",end="|")
        print()
    print(" ","-"*33)



def choosePlayer():
   
    while (True):
        answer = input("\nWould you like to play Black or White?\nPress B for Black οr W for White: ")
        if (answer.upper() != "B" and answer.upper() != "W"):
            print("Invalid option.")
            continue
        break
    if (answer.upper()=="B"):
        return 0    
    elif (answer.upper()=="W"):
        return 1    

def checkIfCanPlay(board, color):
    
    for i in range(N):
        for j in range(N):
            if (validPlaceOne(board,i,j,color)):
                return True
    return False

def hasFilled(board):
    # whether board has been filled
    for i in range(N):
        for j in range (N):
            if (board[i][j]==None):
                return False
    return True


def hasEnded(board):
    if (hasFilled(board)):
        return True
    if (not checkIfCanPlay(board, 0) and not checkIfCanPlay(board, 1)):
        return True
    return False



def validPlaceOne(board, row, col, color):
    return validPlaceTwo(board, row, col, color)



def validPlaceTwo(board, row, col, color):
    if board[row][col] is not None:
        return None

    opponent = 1 - color
    flipped_discs = []

    # 8 directions: diagonals, verticals, and horizontals
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),          (0, 1),
                  (1, -1),  (1, 0), (1, 1)]

    for dx, dy in directions:
        x, y = row + dx, col + dy
        temp_flips = []

        while 0 <= x < N and 0 <= y < N and board[x][y] == opponent:
            temp_flips.append((x, y))
            x += dx
            y += dy

        if 0 <= x < N and 0 <= y < N and board[x][y] == color and len(temp_flips) > 0:
            flipped_discs.extend(temp_flips)

    return flipped_discs if flipped_discs else None



def isOnBoard(x, y):
    # whether coordinates are on board
    return x >= 0 and x < N and y >= 0 and y < N


def getPlayerMove(board): 
    while (True):
        print("\nPlease enter the coordinates (ex. a3) of the cell you wish to place your piece: ", end = "")
        pmove = input().lower()

        if (len(pmove) != 2):
            print("Invalid input. \nMust enter two charcters: coloumn character (A-H) and row number (1-8) of cell. \nTry again.")
            continue

        if ((not pmove[0].isdigit()) and pmove[1].isdigit()):   #char number format
            pcol = ord(pmove[0]) - 97   
            prow = int(pmove[1]) - 1    
        elif (pmove[0].isdigit() and (not pmove[1].isdigit())): #number char format
            prow = ord(pmove[1]) - 97   
            pcol = int(pmove[0]) - 1    # numbers on board start from 1
        else:
            print("Invalid input. \nMust enter coloumn character (A-H) and row number (1-8) of cell. \nTry again.")
            continue

        if (not isOnBoard(prow, pcol)): #coordinates must be within board bounds
            print("Invalid input. \nMust enter coloumn character (A-H) and row number (1-8) of cell. \nTry again.")
            continue
        
        vPl = validPlaceOne(board, prow, pcol, s)
        if (vPl == None): 
            print("Invalid input. \nNot a valid move. Try again.")
            continue
        
        for c in vPl: # change symbol of attacked cells
            board[c[0]][c[1]] = s
        break

    return (prow, pcol)


def getChildren(board, color):
    children = []
    for i in range(N):
        for j in range(N):
            isValid = validPlaceOne(board, i, j, color)
            if isValid is not None:
                # Create a deep copy of the board
                new_board = [[board[x][y] for y in range(N)] for x in range(N)]
                for c in isValid:
                    new_board[c[0]][c[1]] = color
                new_board[i][j] = color
                children.append((new_board, (i, j)))  # Only board and move
    return children



def miniMax(board, turn, player):
    return maxNode(board, 0, float('-inf'), float('inf'), player)[1:]
#maximizes AI's points
def maxNode(board, depth, alpha, beta, player):
    if hasEnded(board) or depth == MAX_DEPTH:
        return (evaluateBoard(board, player), None, None)

    best_val = float('-inf')
    best_move = None

    for child in getChildren(board, player):
       child_board, move = child
       val, _, _ = minNode(child_board, depth + 1, alpha, beta, player)
       if val > best_val:
            best_val = val
            best_move = move
            alpha = max(alpha, best_val)
       if beta <= alpha:
            break
    if best_move is not None:
        return (best_val, best_move[0], best_move[1])
    else:
        return (evaluateBoard(board, player), None, None)
MAX_DEPTH = 4  
# key factors in determining current position
WEIGHTS = {
    'corner': 25,
    'edge': 5,
    'mobility': 2,
    'parity': 1
}


#minimizes opponents points
def minNode(board, depth, alpha, beta, player):
    if hasEnded(board) or depth == MAX_DEPTH:
        return (evaluateBoard(board, player), None, None)

    opponent = 1 - player
    best_val = float('inf')
    best_move = None
    for child in getChildren(board, player):
       child_board, move = child
       val, _, _ = maxNode(child_board, depth + 1, alpha, beta, player)
       if val < best_val:
            best_val = val
            best_move = move
            beta = min(beta, best_val)
       if beta <= alpha:
            break
    if best_move is not None:
        return (best_val, best_move[0], best_move[1])
    else:
        return (evaluateBoard(board, player), None, None)


def getScore(board):
    # calculate score
    xscore = 0
    oscore = 0
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                xscore += 1
            if board[i][j] == 1:
                oscore += 1
    return (xscore, oscore)


def printScore(board): 
    print("The final score is......")
    fscore = getScore(board)

    print("Player score: ",fscore[s], "\nComputer score: ",fscore[(1 if s==0 else 0)])
    print(("Player" if fscore[s]>fscore[(1 if s==0 else 0)] else "Computer"), " wins!")
   
    print("\N{trophy}"*20)
    return


def playAgain():
    while (True):
        answer = input("\nDo you want to play again? \nPress y for Yes οr n for No: ")
        if (answer.upper() !="Y" and answer.upper()!="N"):
            print("Invalid option.")
            continue
        break
    print()
    if (answer.upper()=="Y"):
        play()
        playAgain()
    elif (answer.upper()=="N"):
        print ("The game will be terminated.")
        exit()


def play():
    global N
    N = 8
    board = [[None for i in range(N)] for j in range(N)] 
    
    global turnTracker
    global s 
    s = choosePlayer()
    print('\n"X" is Black (goes first), "O" is White\n')


    if (s == 1): #if player choose to play first
        turnTracker = 0    
    else:
        turnTracker = 1

    board[3][3] = 1 
    board[3][4] = 0 
    board[4][3] = 0
    board[4][4] = 1
    
    while(True):
     print()
     printer(board)

     if (turnTracker == 0):  # computer plays
        ai_color = (1 if s == 0 else 0)
        print("It's the computer's turn (", ("O" if s == 0 else "X"), ").")

        children = getChildren(board, ai_color)

        print("Checking legal moves for AI (X)...")
        if children:
            for child in children:
                move = child[1]
                print(f"→ Legal move at ({move[0]}, {move[1]}) → {chr(move[1] + 97)}{move[0] + 1}")
        else:
            print("→ No legal moves found for AI.")

        if children:
            print("AI evaluated this move with score:", evaluateBoard(board, ai_color))

            moveComp = miniMax(board, turnTracker, ai_color)
            if moveComp[0] is not None and moveComp[1] is not None:
                print(f"\n Computer move: ( {chr(moveComp[1] + 97)} , {moveComp[0] + 1} )")
                vCom = validPlaceOne(board, moveComp[0], moveComp[1], ai_color)
                if vCom is not None:
                    board[moveComp[0]][moveComp[1]] = ai_color
                    for c in vCom:
                        board[c[0]][c[1]] = ai_color
            else:
                print("computer has no valid moves.")            
        else:
            print("No available moves for computer.")
     
    
        turnTracker = (turnTracker + 1) % 2


     else:  # player plays
        print("It's the player's turn (", ("X" if s == 0 else "O"), ").")
        if checkIfCanPlay(board, s):
            movePl = getPlayerMove(board)
            board[movePl[0]][movePl[1]] = s
        else:
            print("No available moves for player.")
        turnTracker = (turnTracker + 1) % 2  


     print()
     if hasEnded(board):
        break

    printer(board)
    printScore(board)
    playAgain()
    return

# GAME START
play()
