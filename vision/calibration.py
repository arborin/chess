import cv2

# შენი 4K ფოტოს სახელი
IMAGE_PATH = "first.jpg"

points = []

def mouse_callback(event, x, y, flags, param):
    global points, img_copy
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append([x, y])
        print(f"წერტილი {len(points)}: [{x}, {y}]")
        
        # წერტილის დახატვა ეკრანზე
        cv2.circle(img_copy, (x, y), 10, (0, 255, 0), -1)
        cv2.putText(img_copy, str(len(points)), (x + 15, y + 15), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
        cv2.imshow("Click 4 Corners (A8 -> H8 -> H1 -> A1)", img_copy)
        
        if len(points) == 4:
            print("\n" + "="*40)
            print("✅ დაკოპირე ეს მასივი შენს ძირითად კოდში:")
            print("="*40)
            print("BOARD_CORNER_PTS = np.float32([")
            print(f"    [{points[0][0]}, {points[0][1]}],  # 1. Top-Left (A8)")
            print(f"    [{points[1][0]}, {points[1][1]}],  # 2. Top-Right (H8)")
            print(f"    [{points[2][0]}, {points[2][1]}],  # 3. Bottom-Right (H1)")
            print(f"    [{points[3][0]}, {points[3][1]}]   # 4. Bottom-Left (A1)")
            print("])")
            print("="*40 + "\n")

img = cv2.imread(IMAGE_PATH)
if img is None:
    print(f"❌ ფაილი {IMAGE_PATH} ვერ მოიძებნა!")
    exit()

img_copy = img.copy()

cv2.namedWindow("Click 4 Corners (A8 -> H8 -> H1 -> A1)", cv2.WINDOW_NORMAL)
# ფანჯრის ზომის შემცირება, რომ ეკრანზე დაეტიოს
h, w = img.shape[:2]
cv2.resizeWindow("Click 4 Corners (A8 -> H8 -> H1 -> A1)", w // 2, h // 2)

cv2.setMouseCallback("Click 4 Corners (A8 -> H8 -> H1 -> A1)", mouse_callback)

print("📍 დააკლიკე 4 კუთხეს თანმიმდევრობით:")
print("1. A8 (ზედა-მარცხენა)")
print("2. H8 (ზედა-მარჯვენა)")
print("3. H1 (ქვედა-მარჯვენა)")
print("4. A1 (ქვედა-მარცხენა)")

cv2.imshow("Click 4 Corners (A8 -> H8 -> H1 -> A1)", img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()