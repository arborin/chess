import cv2
import time
import numpy as np

# კამერის ჩართვა (თუ არ იმუშავა, შეცვალეთ 1-ით ან 2-ით)
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# 4K რეზოლუცია
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)



def capture(cap, img_name):
    if not cap.isOpened():
        print("❌ კამერა ვერ ჩაირთო!")
        exit()

    # რამდენიმე ფრეიმის გატარება, რომ ავტოფოკუსმა და ექსპოზიციამ გასწორება მოასწროს
    for _ in range(10):
        cap.read()

    ret, frame = cap.read()

    if ret:
        cv2.imwrite(img_name, frame)
        print("📸 ფოტო წარმატებით შეინახა (silent capture): first_2.jpg")
    else:
        print("❌ ფოტოს გადაღება ვერ მოხერხდა.")

    # cap.release()



# სურათის ამოჭრა

BOARD_CORNER_PTS = np.float32([
    [568, 102],  # 1. Top-Left (A8)
    [1342, 116],  # 2. Top-Right (H8)
    [1414, 928],  # 3. Bottom-Right (H1)
    [512, 932]   # 4. Bottom-Left (A1)
])

def crop_save_and_preview(image_path, save_path="cropped.jpg", output_size=1600):
    img = cv2.imread(image_path)
    if img is None:
        print(f"❌ ფაილი ვერ მოიძებნა: {image_path}")
        return None

    dst_pts = np.float32([
        [0, 0],
        [output_size, 0],
        [output_size, output_size],
        [0, output_size]
    ])

    matrix = cv2.getPerspectiveTransform(BOARD_CORNER_PTS, dst_pts)
    warped = cv2.warpPerspective(img, matrix, (output_size, output_size))
    
    # 1. შენახვა
    cv2.imwrite(save_path, warped)
    print(f"✅ მოჭრილი სურათი შენახულია: {save_path}")

    # 2. ჩვენება (ეკრანზე რომ დაეტიოს, 800x800-მდე ვამცირებთ მხოლოდ სანახავად)
    cv2.namedWindow("Cropped Board Preview", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Cropped Board Preview", 800, 800)
    cv2.imshow("Cropped Board Preview", warped)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return warped


def detect_chess_move(img1_path, img2_path, min_change_threshold=50000):
    img1 = cv2.imread(img1_path)
    img2 = cv2.imread(img2_path)

    if img1 is None or img2 is None:
        print("❌ შეცდომა: სურათების ჩატვირთვა ვერ მოხერხდა!")
        return None

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

            x1 = col_idx * sq_size + margin
            y1 = row_idx * sq_size + margin
            x2 = (col_idx + 1) * sq_size - margin
            y2 = (row_idx + 1) * sq_size - margin

            crop1 = gray1[y1:y2, x1:x2]
            crop2 = gray2[y1:y2, x1:x2]

            diff = cv2.absdiff(crop1, crop2)
            differences[sq_name] = int(np.sum(diff))

    sorted_sqs = sorted(differences, key=lambda k: differences.get(k, 0), reverse=True)
    
    sq1, sq2 = sorted_sqs[0], sorted_sqs[1]
    score1, score2 = differences[sq1], differences[sq2]

    # შემოწმება: არის თუ არა ცვლილება საკმარისად დიდი
    if score1 < min_change_threshold:
        print(f"ℹ️ სვლა არ დაფიქსირებულა (მაქსიმალური განსხვავება: {score1})")
        return None

    print(f"🔍 დაფიქსირდა ცვლილება უჯრებზე: {sq1.upper()} ({score1}) და {sq2.upper()} ({score2})")
    return sq1, sq2






if __name__ == "__main__":
    # capture(cap, "first.jpg")
    # time.sleep(10)
    # capture(cap, "second.jpg")
    # time.sleep(2)
    # crop_save_and_preview("first.jpg", "first_croped.jpg")
    # time.sleep(2)
    # crop_save_and_preview("second.jpg", "second_croped.jpg")
    # გაშვება შენს ფაილებზე
    detect_chess_move("cropped_1.jpg", "cropped_2.jpg")


