import cv2
import numpy as np

import cv2
import numpy as np

def debug_chess_move(img1_path, img2_path):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("❌ სურათები ვერ ჩაიტვირთა!")
        return

    # ზომის სტანდარტიზაცია
    img1 = cv2.resize(img1, (1600, 1600))
    img2 = cv2.resize(img2, (1600, 1600))
    sq_size = 200

    gray1 = cv2.GaussianBlur(cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY), (5, 5), 0)
    gray2 = cv2.GaussianBlur(cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY), (5, 5), 0)

    files = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    ranks = [8, 7, 6, 5, 4, 3, 2, 1]

    differences = {}
    margin = 25

    for row_idx, rank in enumerate(ranks):
        for col_idx, file_letter in enumerate(files):
            sq_name = f"{file_letter}{rank}"

            # კოორდინატების გამოთვლა
            x1 = col_idx * sq_size + margin
            y1 = row_idx * sq_size + margin
            x2 = (col_idx + 1) * sq_size - margin
            y2 = (row_idx + 1) * sq_size - margin

            crop1 = gray1[y1:y2, x1:x2]
            crop2 = gray2[y1:y2, x1:x2]

            diff = cv2.absdiff(crop1, crop2)
            differences[sq_name] = int(np.sum(diff))

    # დავლაგოთ და დაბეჭდოთ ტოპ-5 უჯრა
    sorted_sqs = sorted(differences, key=lambda k: differences.get(k, 0), reverse=True)

    print("--- 📊 ტოპ 5 ცვლილება ---")
    for i in range(5):
        sq = sorted_sqs[i]
        print(f"{i+1}. უჯრა: {sq.upper()} -> ქულა: {differences[sq]}")

if __name__ == "__main__":
    debug_chess_move("cropped_1.jpg", "cropped_2.jpg")