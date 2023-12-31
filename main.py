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

# ----------------- HARD
def evaluate_position(board, player, IA):
  if verify_winner(board, IA):
    return 1
  elif verify_winner(board, player):
    return -1
  return 0

def minimax(board, depth, max_depth, maximizing_player, player, IA, n = 0):
  if depth == max_depth or verify_winner(board, IA) or verify_winner(board, player) or is_board_full(board):
    return evaluate_position(board, player, IA), n

  if maximizing_player:
    max_score = float('-inf')
    for i in range(len(board)):
      for j in range(len(board[i])):
        if board[i][j] == "":
          board[i][j] = IA
          score, n = minimax(board, depth + 1, max_depth, False, player, IA, n + 1)
          board[i][j] = ""
          max_score = max(max_score, score)
    return max_score, n
  else:
    min_score = float('inf')
    for i in range(len(board)):
      for j in range(len(board[i])):
        if board[i][j] == "":
          board[i][j] = player
          score, n = minimax(board, depth + 1, max_depth, True, player, IA, n + 1)
          board[i][j] = ""
          min_score = min(min_score, score)
    return min_score, n
  
def hard(board, player, IA):
  best_score = float('-inf')
  best_move = None
  min_depth = float('inf')
  
  for i in range(len(board)):
    for j in range(len(board[i])):
      if board[i][j] == "":
        board[i][j] = IA
        score, n = minimax(board, 0, 9, False, player, IA)
        board[i][j] = ""
        
        if score > best_score:
          best_score = score
          best_move = (i, j)
        elif score == best_score:
          if min_depth > n:
            best_move = (i, j)
            min_depth = n
  return best_move

# ----------------- MEDIUM
def medium(board, player, IA):
  for i in range(3):
    count_IA = 0
    count_player = 0
    empty_indices = -1
      
    for j in range(3):
      if board[i][j] == IA:
        count_IA += 1
      elif board[i][j] == player:
        count_player += 1
      else:
        empty_indices = j
      
    if count_player == 2 and count_IA == 0:
      return (i, empty_indices)
    elif count_IA == 2 and count_player == 0:
      return (i, empty_indices)

  for j in range(3):
    count_IA = 0
    count_player = 0
    empty_indices = -1
    
    for i in range(3):
      if board[i][j] == IA:
        count_IA += 1
      elif board[i][j] == player:
        count_player += 1
      else:
        empty_indices = i
    
    if count_player == 2 and count_IA == 0:
      return (empty_indices, j)
    elif count_IA == 2 and count_player == 0:
      return (empty_indices, j)

    if board[0][0] == player and board[1][1] == player and board[2][2] == "":
      return (2, 2)
    elif board[0][0] == player and board[2][2] == player and board[1][1] == "":
      return (1, 1)
    elif board[1][1] == player and board[2][2] == player and board[0][0] == "":
      return (0, 0)
    elif board[0][2] == player and board[1][1] == player and board[2][0] == "":
      return (2, 0)
    elif board[0][2] == player and board[2][0] == player and board[1][1] == "":
      return (1, 1)
    elif board[1][1] == player and board[2][0] == player and board[0][2] == "":
      return (0, 2)
    
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

# ----------------- EASY
class Node:
  def __init__(self, board, move):
    self.board = board
    self.move = move
    self.children = []

  def add_child(self, child):
    self.children.append(child)

def generate_moves(board):
  moves = []
  for i in range(3):
    for j in range(3):
      if board[i][j] == "":
          moves.append((i, j))
  return moves

def apply_move(board, move, symbol):
  new_board = [row[:] for row in board]
  new_board[move[0]][move[1]] = symbol
  return new_board

def easy(board, IA):
  root = Node(board, None)
  queue = []
  queue.append(root)

  while queue:
    current_node = queue.pop(0)
    if verify_winner(current_node.board, IA):
      return current_node.move

    possible_moves = generate_moves(current_node.board)
    for move in possible_moves:
      child_board = apply_move(current_node.board, move, IA)
      child_node = Node(child_board, move)
      current_node.add_child(child_node)
      queue.append(child_node)

  return random_move(board)

def IA(board, player, IA):
  if session.get("difficulty") == "Hard":
    return hard(board, player, IA)
  elif session.get("difficulty") == "Medium":
    return medium(board, player, IA)
  elif session.get("difficulty") == "Easy":
    return easy(board, IA)
