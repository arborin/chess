import cv2
import numpy as np

clicked_points = []

def mouse_handler(event, x, y, flags, param):
    global clicked_points, img_preview
    if event == cv2.EVENT_LBUTTONDOWN and len(clicked_points) < 4:
        clicked_points.append((x, y))
        cv2.circle(img_preview, (x, y), 15, (0, 255, 0), -1)
        cv2.putText(img_preview, str(len(clicked_points)), (x + 20, y + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)
        cv2.imshow("Click 4 corners of PLAYING AREA", img_preview)
        if len(clicked_points) == 4:
            cv2.waitKey(300)
            cv2.destroyAllWindows()

# 1. სურათის ჩატვირთვა
input_filename = "first.jpg"
img = cv2.imread(input_filename)

if img is None:
    print(f"❌ {input_filename} ვერ მოიძებნა!")
    exit()

img_preview = img.copy()

cv2.namedWindow("Click 4 corners of PLAYING AREA", cv2.WINDOW_NORMAL)
h, w = img_preview.shape[:2]
cv2.resizeWindow("Click 4 corners of PLAYING AREA", w // 2, h // 2)
cv2.setMouseCallback("Click 4 corners of PLAYING AREA", mouse_handler)

print("🖼️ დააჭირეთ უშუალოდ სათამაშო ველის (ჭადრაკის უჯრების) 4 კუთხეს:")
print("1. A8 უჯრის ზედა-მარცხენა კუთხე")
print("2. H8 უჯრის ზედა-მარჯვენა კუთხე")
print("3. H1 უჯრის ქვედა-მარჯვენა კუთხე")
print("4. A1 უჯრის ქვედა-მარცხენა კუთხე")

cv2.imshow("Click 4 corners of PLAYING AREA", img_preview)

while len(clicked_points) < 4:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        exit()

# 2. მხოლოდ დაფის ამოჭრა და პერსპექტივის გასწორება
pts1 = np.float32(clicked_points)
size = 2000
pts2 = np.float32([[0, 0], [size, 0], [size, size], [0, size]])

matrix = cv2.getPerspectiveTransform(pts1, pts2)
warped_board = cv2.warpPerspective(img, matrix, (size, size))

# ინახავს მხოლოდ ამოჭრილ, გასწორებულ დაფას
cv2.imwrite("warped_board.jpg", warped_board)
print("✅ ამოჭრილი დაფა შენახულია: warped_board.jpg")

# 3. 8x8 ბადის დადება ამოჭრილ დაფაზე
grid_img = warped_board.copy()
sq_h = size // 8
sq_w = size // 8

files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
ranks = ['8', '7', '6', '5', '4', '3', '2', '1']

for r_idx, rank in enumerate(ranks):
    for f_idx, file in enumerate(files):
        x1 = f_idx * sq_w
        y1 = r_idx * sq_h
        x2 = (f_idx + 1) * sq_w
        y2 = (r_idx + 1) * sq_h

        square_name = f"{file}{rank}"

        # მწვანე ჩარჩო თითოეულ უჯრას
        cv2.rectangle(grid_img, (x1, y1), (x2, y2), (0, 255, 0), 3)

        # წითელი ტექსტი უჯრის ცენტრში
        text_x = x1 + int(sq_w * 0.2)
        text_y = y1 + int(sq_h * 0.6)
        cv2.putText(grid_img, square_name, (text_x, text_y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3, cv2.LINE_AA)

# შედეგის შენახვა და ჩვენება
cv2.imwrite("grid_preview.jpg", grid_img)
print("✅ ბადე დატანილია: grid_preview.jpg")

resized_preview = cv2.resize(grid_img, (800, 800))
cv2.imshow("Only Board with 8x8 Grid", resized_preview)
cv2.waitKey(0)
cv2.destroyAllWindows()