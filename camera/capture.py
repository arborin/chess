import cv2

# 0 ჩვეულებრივ მთავარი კამერის ინდექსია. 
# თუ კამერა არ ჩაირთო, სცადეთ 1 ან 2
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows-ზე CAP_DSHOW აუმჯობესებს 4K მხარდაჭერას

# კამერის რეზოლუციის დაყენება (4K / 1080p)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 3840)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 2160)

if not cap.isOpened():
    print("❌ კამერა ვერ ჩაირთო! შეამოწმეთ მიერთება ან ინდექსი (0, 1, 2).")
    exit()

print("📸 კამერა ჩართულია!")
print(" - დააჭირეთ 'Space' (ჰარი) ფოტოს გადასაღებად")
print(" - დააჭირეთ 'Q' ან 'ESC' გასასვლელად")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ ფრეიმის წაკითხვა ვერ მოხერხდა.")
        break

    # ეკრანზე საჩვენებლად ზომის შემცირება (4K ფანჯარა ეკრანზე რომ დაეტიოს)
    preview_frame = cv2.resize(frame, (960, 540))
    cv2.imshow("Chess Camera Preview - Press SPACE to Capture", preview_frame)

    key = cv2.waitKey(1) & 0xFF

    # Space ღილაკზე დაჭერით იღებს სრულ (4K) რეზოლუციის ფოტოს
    if key == 32:  # ASCII for Space
        filename = "first_2.jpg"
        cv2.imwrite(filename, frame)
        print(f"✅ ფოტო წარმატებით შენახდა: {filename}")
        break

    # Q ან ESC ღილაკით გამოსვლა
    elif key == ord('q') or key == 27:
        print("გამოსვლა...")
        break

cap.release()
cv2.destroyAllWindows()