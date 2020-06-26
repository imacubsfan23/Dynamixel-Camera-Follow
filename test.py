import pyautogui
import handy
import cv2

res = pyautogui.size()
camera_res = (720,480)#480p so response time of hand movement is faster

# capture the hand histogram by placing your hand in the box shown and
# press 'A' to confirm
# source is set to inbuilt webcam by default. Pass source=1 to use an
# external camera.
hist = handy.capture_histogram(0)

# getting video feed from webcam
cap = cv2.VideoCapture(0)

while True:
    k = cv2.waitKey(1)
    # Press 'esc' to exit
    if k%256 == 27:
        break

    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, camera_res)

    if not ret:
        break

    # to block a faces in the video stream, set block=True.
    # if you just want to detect the faces, set block=False
    # if you do not want to do anything with faces, remove this line
    # handy.detect_face(frame, block=True)

    # detect the hand
    hand = handy.detect_hand(frame, hist)

    # to get the outline of the hand
    # min area of the hand to be detected = 10000 by default
    custom_outline = hand.draw_outline(
        min_area=1000, color=(0, 255, 255), thickness=2)

    # to get a quick outline of the hand
    quick_outline = hand.outline

    # draw fingertips on the outline of the hand, with radius 5 and color red,
    # filled in.
    #for fingertip in hand.fingertips:
    #    cv2.circle(quick_outline, fingertip, 5, (0, 0, 255), -1)

    # to get the centre of mass of the hand
    com = hand.get_center_of_mass()
    if com:
        cv2.circle(quick_outline, com, 10, (255, 0, 0), -1)

    #shows camera
    cv2.imshow("Handy", quick_outline)

    mouse_pos = (camera_res[0]/2, camera_res[1]/2)
    try:
        #mapping camera position to screen position
        mouse_pos = (com[0] * (res[0]/camera_res[0]),com[1] * (res[1]/camera_res[1]))
        pyautogui.moveTo(mouse_pos, duration = 0)
    except:
        pass
cap.release()
cv2.destroyAllWindows()
