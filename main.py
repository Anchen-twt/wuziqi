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
  count = 0
   
  for x in range(SIZE):
    for y in range(SIZE):
      if board[x][y] == player:
        series_count = 1
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
    try:
      row = int(input('请输入行(1-'+str(SIZE)+'):'))-1
      col = int(input('请输入列(1-'+str(SIZE)+'):'))-1
    except:
      continue
      
    if valid_move(row, col):
      break
  board[row][col] = 1

# 评估函数
def evaluate(board): 
  score = 0
  # 评估活二数量
  my_live_two = count_all_series(board, 2, 2)
  score += my_live_two * 32

  opponent_live_two = count_all_series(board, 1, 2)  
  score -= opponent_live_two * 48
  
  # 评估活三数量
  my_live_three = count_all_series(board, 2, 3)
  score += my_live_three * 160

  opponent_live_three = count_all_series(board, 1, 3)  
  score -= opponent_live_three * 240

  # 评估活四数量
  my_live_four = count_all_series(board, 2, 4)
  score += my_live_four * 800
    
  opponent_live_four = count_all_series(board, 1, 4)
  score -= opponent_live_four * 1200
  
  # 评估胜利
  if check_win(2):
    score += 4000
    
  elif check_win(1):        
    score -= 6000
  
  # 评估占据中点的加分
  if board[7][7] == 2:
    score += 30
  elif board[7][7] == 1: 
    score -= 15
    
  # 评估占据角点的加分
  corner = [0,0], [0,14], [14,0], [14,14] 
  for i, j in corner:
    if board[i][j] == 2:
      score += 10
    elif board[i][j] == 1:
      score -= 5
      
  return score

# 深度优先搜索算法
def dfs(depth, player):
 
  # depth为搜索深度,player表示当前玩家
 
  # 当深度为0时,直接返回当前状态的评估分数
  if depth == 0:
    return evaluate(board)
 
  # 初始最佳分数
  best_score = -9999 if player == 2 else 9999 
 
  # 遍历每一个可能的落子点
  for row in range(SIZE):
    for col in range(SIZE):       
      # 如果当前点为空
      if board[row][col] == 0:
       
        # 落子 
        board[row][col] = player
         
        # 切换玩家,搜索下一层
        score = -dfs(depth - 1, 3 - player)
         
        # 撤销落子
        board[row][col] = 0
         
        # 更新最佳分数
        best_score = max(score, best_score) if player == 2 else min(score, best_score)
   
  return best_score
   
# 电脑移动函数
def computer_move(): 
  best_score = -9999
  # 搜索步数
  depth = 2
   
  for row in range(SIZE):
    for col in range(SIZE):     
      if valid_move(row, col):     
        board[row][col] = 2
        # DFS搜索评分
        score = -dfs(depth-1, 2)
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