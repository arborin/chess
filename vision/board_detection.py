# img = load_image(r"D:\projects\chess\images\board.jpg")

import cv2
import numpy as np

# ----------------------------
# Split board
# ----------------------------
def split_board(img):
    h, w = img.shape[:2]
    dh, dw = h // 8, w // 8

    squares = []
    for y in range(8):
        row = []
        for x in range(8):
            sq = img[y*dh:(y+1)*dh, x*dw:(x+1)*dw]
            row.append(sq)
        squares.append(row)
    return squares


# ----------------------------
# Crop center (ignore borders)
# ----------------------------
def crop_center(square):
    h, w = square.shape[:2]
    return square[int(h*0.2):int(h*0.8), int(w*0.2):int(w*0.8)]


# ----------------------------
# Detect if square has piece
# ----------------------------
def has_piece(square):
    square = crop_center(square)

    gray = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)

    # Edge detection (key improvement)
    edges = cv2.Canny(gray, 50, 150)

    edge_count = np.sum(edges > 0)
    total = square.shape[0] * square.shape[1]

    ratio = edge_count / total

    return ratio > 0.02   # tune this


# ----------------------------
# Detect piece color
# ----------------------------
def get_piece_color(square):
    square = crop_center(square)

    gray = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
    mean = np.mean(gray)

    return "white" if mean > 140 else "black"


# ----------------------------
# Detect board
# ----------------------------
def detect_board(img):
    img = cv2.resize(img, (800, 800))  # normalize
    squares = split_board(img)

    board = []

    for row in squares:
        board_row = []
        for sq in row:
            if not has_piece(sq):
                board_row.append(".")
            else:
                color = get_piece_color(sq)
                board_row.append("W" if color == "white" else "B")

        board.append(board_row)

    return board


# ----------------------------
# Print board
# ----------------------------
def print_board(board):
    for row in board:
        print(" ".join(row))


# ----------------------------
# MAIN
# ----------------------------
img = cv2.imread(r"D:\projects\chess\images\board.jpg")
# img = load_image(r"D:\projects\chess\images\board.jpg")

board = detect_board(img)
print_board(board)