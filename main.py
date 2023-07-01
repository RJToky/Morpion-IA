from flask import Flask, request, session
from flask import render_template
import json
import random

app = Flask(__name__, static_url_path="/static")
app.secret_key = "1822"

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/play", methods=["GET"])
def play(difficulty = "Medium", player = "X"):
  session["board"] = [
    ["", "", ""],
    ["", "", ""],
    ["", "", ""]
  ]
  
  if request.args.get("difficulty") and request.args.get("player"):
    session["difficulty"] = request.args.get("difficulty")
    session["player"] = request.args.get("player")
    session["IA"] = "O" if session["player"] == "X" else "X"
    
    data = {
      "board": session.get("board"),
      "difficulty": session.get("difficulty"),
      "player": session.get("player")
    }
    return index()
  
  if not session.get("difficulty") and not session.get("player"):
    session["difficulty"] = difficulty
    session["player"] = player
    session["IA"] = "O" if session["player"] == "X" else "X"
  
  data = {
    "board": session.get("board"),
    "difficulty": session.get("difficulty"),
    "player": session.get("player")
  }
  return json.dumps(data)

@app.route("/process", methods=["GET"])
def process():
  board = session.get("board")
  current_player = request.args.get("current_player")
  
  if current_player == session.get("player"):
    row = int(request.args.get("row"))
    col = int(request.args.get("col"))
  
    if board[row][col] == "":
      board[row][col] = current_player  

  elif current_player == session.get("IA"):
    row, col = random_move(board) if is_board_empty(board) else IA(board, session.get("player"), session.get("IA"))
    board[row][col] = current_player
  
  session["board"] = board
  current_player = "O" if current_player == "X" else "X"

  data = {
    "board": session.get("board"),
    "difficulty": session.get("difficulty"),
    "current_player": current_player,
    "winner": verify_winner(session.get("board"), request.args.get("current_player")),
    "board_full": is_board_full(session.get("board"))
  }
  return json.dumps(data)

def is_board_empty(board):
  for row in board:
    for cell in row:
      if cell != "":
        return False
  return True

def is_board_full(board):
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == "":
        return False
  return True

def verify_winner(board, player):
  for i in range(len(board)):
    if board[i][0] == board[i][1] == board[i][2] == player:
      return True
  for j in range(len(board)):
    if board[0][j] == board[1][j] == board[2][j] == player:
      return True
  if board[0][0] == board[1][1] == board[2][2] == player:
    return True
  if board[0][2] == board[1][1] == board[2][0] == player:
    return True
  return False

def random_move(board):
  list_choice = [0, 1, 2]
  while 1 < 2:
    i = random.choice(list_choice)
    j = random.choice(list_choice)
    if board[i][j] == "":
      return (i, j)

def evaluate_position(board, player, IA):
  if verify_winner(board, IA):
    return 1
  elif verify_winner(board, player):
    return -1
  return 0

def minimax(board, depth, max_depth, maximizing_player, player, IA):
  if depth == max_depth or verify_winner(board, IA) or verify_winner(board, player) or is_board_full(board):
    return evaluate_position(board, player, IA), depth

  if maximizing_player:
    max_score = float('-inf')
    for i in range(len(board)):
      for j in range(len(board[i])):
        if board[i][j] == "":
          board[i][j] = IA
          score, depth = minimax(board, depth + 1, max_depth, False, player, IA)
          board[i][j] = ""
          max_score = max(max_score, score)
    return max_score, depth
  else:
    min_score = float('inf')
    for i in range(len(board)):
      for j in range(len(board[i])):
        if board[i][j] == "":
          board[i][j] = player
          score, depth = minimax(board, depth + 1, max_depth, True, player, IA)
          board[i][j] = ""
          min_score = min(min_score, score)
    return min_score, depth

# ----------------- HARD
def hard(board, player, IA):
  best_score = float('-inf')
  best_move = None
  min_depth = float('inf')
  
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == "":
        board[i][j] = IA
        score, depth = minimax(board, 0, 9, False, player, IA)
        board[i][j] = ""
        
        if score > best_score:
          best_score = score
          best_move = (i, j)
        elif score == best_score:
          if min_depth > depth:
            best_move = (i, j)
            min_depth = depth
  return best_move

# ----------------- MEDIUM 
def medium(board, player, IA):
  best_score = float('-inf')
  best_move = None
  
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == "":
        board[i][j] = IA
        score, _ = minimax(board, 0, 1, False, player, IA)
        board[i][j] = ""
        
        if score > best_score:
          best_score = score
          best_move = (i, j)
  return best_move

# ----------------- EASY
def easy(board, player, IA):
  for i in range(3):
    count_IA = 0
    count_player = 0
    empty_indices = []
    
    for j in range(3):
      if board[i][j] == IA:
        count_IA += 1
      elif board[i][j] == player:
        count_player += 1
      else:
        empty_indices.append(j)
    
    if count_IA == 2 and count_player == 0:
      return (i, random.choice(empty_indices))

  for j in range(3):
    count_IA = 0
    count_player = 0
    empty_indices = []
    
    for i in range(3):
      if board[i][j] == IA:
        count_IA += 1
      elif board[i][j] == player:
        count_player += 1
      else:
        empty_indices.append(i)
    
    if count_IA == 2 and count_player == 0:
      return (random.choice(empty_indices), j)

  if board[0][0] == IA and board[1][1] == IA and board[2][2] == "":
    return (2, 2)
  elif board[0][0] == IA and board[2][2] == IA and board[1][1] == "":
    return (1, 1)
  elif board[1][1] == IA and board[2][2] == IA and board[0][0] == "":
    return (0, 0)
  elif board[0][2] == IA and board[1][1] == IA and board[2][0] == "":
    return (2, 0)
  elif board[0][2] == IA and board[2][0] == IA and board[1][1] == "":
    return (1, 1)
  elif board[1][1] == IA and board[2][0] == IA and board[0][2] == "":
    return (0, 2)

  return random_move(board)

def IA(board, player, IA):
  if session.get("difficulty") == "Hard":
    return hard(board, player, IA)
  elif session.get("difficulty") == "Medium":
    return medium(board, player, IA)
  elif session.get("difficulty") == "Easy":
    return easy(board, player, IA)

if __name__=="__main__":
  board = [
    ["", "", ""],
    ["", "", ""],
    ["", "", "X"]
  ]
  print(easy(board, "X", "O"))
