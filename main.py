import pygame
import chess
import ctypes
import threading
import win32gui
import win32con
from stockfish import Stockfish

pygame.init()

WIDTH, HEIGHT = 640, 640
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS

WHITE = (240, 217, 181)
BROWN = (181, 136, 99)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("MoveVision")

hwnd = pygame.display.get_wm_info()['window']

# Constants
HWND_TOPMOST = -1
SWP_NOMOVE = 0x0001
SWP_NOSIZE = 0x0002


chess_board = chess.Board()

location = r"C:\Users\admin\Downloads\stockfish\stockfish-windows-x86-64.exe"
rows = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e':4, 'f':5, 'g':6, 'h':7}


print(".......................................................")
print("Init StockFish Engine...")
print(".......................................................")
stockfish = Stockfish(path=location)




piece_images = {}


def force_topmost():
    # 1. Set topmost
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )

    # 2. Bring to foreground (important)
    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
    win32gui.SetForegroundWindow(hwnd)


def load_images():
    pieces = ["wp","wr","wkn","wb","wq","wk",
              "bp","br","bkn","bb","bq","bk"]

    for p in pieces:
        img = pygame.image.load(f"D:\projects\chess\images\pieces\{p}.png")
        img = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))
        piece_images[p] = img



# Board state
board = [
    ["br","bkn","bb","bq","bk","bb","bkn","br"],
    ["bp","bp","bp","bp","bp","bp","bp","bp"],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["","","","","","","",""],
    ["wp","wp","wp","wp","wp","wp","wp","wp"],
    ["wr","wkn","wb","wq","wk","wb","wkn","wr"],
]

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(win, color,
                             (col*SQUARE_SIZE, row*SQUARE_SIZE,
                              SQUARE_SIZE, SQUARE_SIZE))
            
def draw_pieces():
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece != "":
                win.blit(piece_images[piece],
                         (col*SQUARE_SIZE, row*SQUARE_SIZE))
                         


def update_board(start, end):
    
    # print("start-end: ", start, end)
    start_c = start[0]
    start_c = rows[start_c]
    start_r = 8-int(start[1])

    end_c = end[0]
    end_c = rows[end_c]
    end_r = 8-int(end[1])


    # print("===============================")
    # print(start_c, start_r)
    # print("===============================")

    piece = board[start_r][start_c]
    
    board[start_r][start_c] = ""
        
    # print("===============================")
    # print(piece)
    # print("===============================")
    
    board[end_r][end_c] = piece
    


def cli_input():
    global board
    global chess_board
    global stockfish
    
    
    
    # elo = int(input("Set elo: "))
    stockfish.set_elo_rating(1400) 
    
    while True:
        force_topmost()
        user_input = input("Enter new value: (e2 e4): ")
        # Board state
        
        start, end = user_input.split(" ")
        
        update_board(start, end)
        
        move = chess.Move.from_uci(start+end)
        chess_board.push(move)
        
        fen = chess_board.fen()
        
        print("=====================================")
        print("Board FEN: ", fen)
        print("=====================================")
        
        
        stockfish.set_fen_position(fen)
        best_move = stockfish.get_best_move()
        
        sf_start = best_move[0:2]
        sf_end = best_move[2:4]
        print(">>> Stockfish Move: ", best_move)
        print("=====================================")
        update_board(sf_start, sf_end)
        move = chess.Move.from_uci(sf_start+sf_end)
        chess_board.push(move)
        
        
        fen = chess_board.fen()
        
        print("Board FEN: ", fen)
        print("=====================================")
        
        

# Start CLI input thread
threading.Thread(target=cli_input, daemon=True).start()




def banner():
    print("""                                  _        _              
  _ __    ___  __ __  ___  __ __ (_)  ___ (_)  ___   _ _  
 | '  \  / _ \ \ V / / -_) \ V / | | (_-< | | / _ \ | ' \ 
 |_|_|_| \___/  \_/  \___|  \_/  |_| /__/ |_| \___/ |_||_|
                                                          """)
    print("---------------------------------------------------")
                 

def main():
    banner()
    load_images()
    run = True
    clock = pygame.time.Clock()
    
    
    
    
    

    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        draw_board()
        draw_pieces()
        
        
        
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()