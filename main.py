import cv2
import time


def gauss_blur():
    img = cv2.imread('images/variant-2.png')
    height = 600
    width = 800
    res = cv2.resize(img, (width, height), interpolation=cv2.INTER_LINEAR)
    img_blur_7 = cv2.GaussianBlur(res, (15, 15), 0)
    cv2.imshow('img_blur_15', img_blur_7)


def video_processing():
    cap = cv2.VideoCapture(0)
    down_points = (640, 480)
    f = open('coordinates.txt', 'w')
    coord = []
    i = 0
    img = cv2.imread('fly64.png')
    img = cv2.resize(img, (32, 32))
    img_height, img_width, _ = img.shape
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 110, 255, cv2.THRESH_BINARY_INV)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            center = ((int(x + (w // 2) - 16)), int(y + (h // 2) - 16))
            x_center = center[0]
            y_center = center[1]
            frame[y_center:y_center + img_height, x_center:x_center + img_width] = img

            if i % 5 == 0:
                a = x + (w // 2)
                b = y + (h // 2)
                coord.append(a)
                coord.append(b)
                print(a, b)
                f.write(str(coord) + '\n')
                coord.clear()

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)
        i += 1

    cap.release()


if __name__ == '__main__':
    gauss_blur()
    video_processing()
    cv2.waitKey(0)
    cv2.destroyAllWindows()
