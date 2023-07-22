# 定义棋盘大小
SIZE = 15  
 
# 创建空棋盘
board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]  
 
# 显示棋盘
def print_board():
  # 打印列序号,多打印一个空格列对齐
  print('  ', end=' ') 
  for i in range(1, SIZE + 1):
      print(str(i).center(2), end='')  
  print()
    
  # 打印行和棋盘
  for i in range(SIZE):
      # 打印行序号,右对齐占2位
      print(str(i+1).rjust(2), end=' ')   
      for j in range(SIZE):
          print('O' if board[i][j] == 1 else 'X' if board[i][j] == 2 else '+', end=' ')
      print()
 
# 检查落子是否有效
def valid_move(row, col):
  return 0 <= row < SIZE and 0 <= col < SIZE and board[row][col] == 0 
     
# 统计指定方向指定玩家和长度的连子数量        
def count_series(board, player, dx, dy, length):
  series_count = 0
  count = 0
   
  for x in range(SIZE):
      for y in range(SIZE):
          if board[x][y] == player:
              next_x = x + dx
              next_y = y + dy
       
              while 0 <= next_x < SIZE and 0 <= next_y < SIZE and board[next_x][next_y] == player:
                  next_x += dx
                  next_y += dy
                  series_count += 1
             
              if series_count >= length:
                  count += 1
               
  return count               

# 统计指定玩家和长度的连子数量
def count_all_series(board, player, length):
  total = 0
   
  # 水平方向
  total += count_series(board, player, 0, 1, length)   
  # 垂直方向
  total += count_series(board, player, 1, 0, length)   
  # 主对角线方向
  total += count_series(board, player, 1, 1, length)
  # 副对角线方向
  total += count_series(board, player, 1, -1, length)
   
  return total
    
# 玩家落子  
def player_move():
  while True:
      row = int(input('请输入行(1-'+str(SIZE)+'):'))-1
      col = int(input('请输入列(1-'+str(SIZE)+'):'))-1
      if valid_move(row, col):
          break
  board[row][col] = 1
    
# 评估函数
def evaluate(board): 
  score = 0
   
  # 评估当前玩家的活四的数量
  my_live_four = count_all_series(board, 2, 4)
  score += my_live_four * 1000
    
  # 评估对手的活四的数量  
  opponent_live_four = count_all_series(board, 1, 4)
  score -= opponent_live_four * 500

  return score
 
# 电脑移动函数
def computer_move(): 
  best_score = -9999
   
  for row in range(SIZE):
      for col in range(SIZE):     
          if valid_move(row, col):     
              board[row][col] = 2
              score = evaluate(board)
              board[row][col] = 0         
              if score > best_score:         
                  best_row = row
                  best_col = col
                  best_score = score
 
  print('电脑下在 (%d, %d)' % (best_row + 1, best_col + 1))   
  board[best_row][best_col] = 2  
 
# 检查是否胜利
def check_win(player): 
  if count_all_series(board, player, 5) > 0:
      return True 
    
    
    
# 当前玩家  
current_player = 1
 
# 游戏主循环
while True:
  print_board()
  if current_player == 1:
      player_move()  
  else:
      computer_move()
   
  if check_win(current_player):
      print_board()       
      print(current_player, '赢了!')
      break 
   
  # 切换当前玩家
  current_player = 2 if current_player == 1 else 1 
 
print('游戏结束')