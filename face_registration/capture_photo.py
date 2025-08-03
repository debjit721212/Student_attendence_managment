import cv2

def capture_student_photo(student_id):
    cap = cv2.VideoCapture(0)
    print("Press SPACE to capture photo, ESC to exit.")
    while True:
        ret, frame = cap.read()
        cv2.imshow('Capture Photo', frame)
        key = cv2.waitKey(1)
        if key % 256 == 27:  # ESC pressed
            print("Escape hit, closing...")
            break
        elif key % 256 == 32:  # SPACE pressed
            img_name = f"student_{student_id}.jpg"
            cv2.imwrite(img_name, frame)
            print(f"{img_name} saved!")
            break
    cap.release()
    cv2.destroyAllWindows()

# Example usage:
# capture_student_photo("SCHOOL2024-0001")