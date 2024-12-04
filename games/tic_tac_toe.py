class Game:
    
    def __init__(self):
        self.board = [['-' for _ in range(3)] for _ in range(3)]
        self.players = ['X', 'O']
        
    def check_valid_move(self, row: int, col: int) -> bool:
        return 0 <= row < 3 and 0 <= col < 3 and self.board[row][col] == '-'
    
    """
    Returns string of winning player, or empty string if no win 
    """
    def check_win(self) -> str:
        # ways to win: all 3 in a row, col, or in two diagonals 

        # map[row/col/diag_num] = count (+1 for x, -1 for 0)
        # could make hashmap for each and then iterate through board
        # add incr count for row, col, diag 
            # ret winner if count is ever 3
        rows = {i: 0 for i in range(3)}
        cols = {i: 0 for i in range(3)}
        diagonals = {'left': 0, 'right' : 0}
        for i in range(3):
            for j in range(3):
                val = self.board[i][j]
                if val != 'X' and val != 'O':
                    continue
                counter = 1 if val == 'X' else -1
                rows[i] += counter 
                cols[j] += counter 
                
                # have to check the individual ones 
                # 0,0 and 2,2 for left diag 
                # 2, 0 and 0, 2 for right diag
                # 1,1 for both 
                
                if i == j:
                    diagonals['left'] += counter 
                
                if i + j == 2:
                    diagonals['right'] += counter 

                
                if abs(rows[i]) == 3 or abs(cols[j]) == 3 or abs(diagonals["left"]) == 3 or abs(diagonals["right"]) == 3:
                    return val 
                
    """
    memory efficient 
    def check_win(self) -> str:
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != '-':
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != '-':
                return self.board[0][i]

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != '-':
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != '-':
            return self.board[0][2]

        return ''
    """
        
        
    def check_draw(self) -> bool:
        for row in self.board:
            if '-' in row:
                return False
        return True
    
    def print_board(self):
        for row in self.board:
            print(' | '.join(row))
            print('-' * 9)
            
    def bot_move(self):
        best_move = None 
        best_score = float('-inf')
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '-':
                    self.board[i][j] = 'X'
                    score = self.minimax(0, False)
                    self.board[i][j] = '-'
                    if score > best_score:
                        best_score = score 
                        best_move = (i, j)
        
        return best_move
        
    
    def minimax(self, depth: int, bot: bool):

        result = self.check_win()
        if result == 'X':
            return 10 - depth
        elif result == 'O':
            return depth - 10
        elif self.check_draw():
            return 0
        
        if bot:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.board[i][j] = 'X'
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = '-'
                        best_score = max(best_score, score)
            return best_score
                        
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '-':
                        self.board[i][j] = 'O'
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = '-'
                        best_score = min(best_score, score)
            
            return best_score
                    

def main():
    
    tic_tac = Game()
    turn = 0
    
    winner = ""
    
    while True:
        current_player = 'X' if turn % 2 == 0 else 'O'
        
        if current_player == 'O':
            valid = False 
            while not valid:
                row = int(input("Choose row: "))
                col = int(input("Choose col: "))
                valid = tic_tac.check_valid_move(row, col)  
                
                if not valid:
                    print("Try Again")  
            
            tic_tac.board[row][col] = current_player
        
        else:
            
            r, c = tic_tac.bot_move()
            tic_tac.board[r][c] = current_player
            
        tic_tac.print_board()
        
        print('-' * 9)
        
        if tic_tac.check_draw():
            winner = "Draw"
            break 
        
        pos_winner = tic_tac.check_win()
        if pos_winner:
            winner = pos_winner
            break
        
        
        turn += 1
        
        
    print(winner, "Won the Game")
        


if __name__ == "__main__":
    main()