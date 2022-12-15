import sys

import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"


def write_to_file(text, file_name):
    # WRITING TO THE TXT FILE
    index = len(file_name) - 1 - file_name[::-1].index('.')

    file = open("{0}.txt".format(file_name[:index]), "w")
    print(text, file=file)
    file.close()
    print("\nText written to file ({0}.txt)\n".format(file_name[:-4]))


def file_to_str():
    # GETTING TEXT FROM IMAGE
    file_name = input("Enter File Name:")
    lang = input("Select a Language (eng, tur)\n")

    try:
        img = cv2.imread(file_name)
        doc = pytesseract.image_to_string(img, lang=lang)
        write_to_file(doc, file_name)

    except:
        print("Failed!")
    else:
        print("Succes!")


# GETTING TEXT FROM CAMERA
def cam_to_str():

    print("\nOpening the Camera")
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    print("Camera opened!\nPress 'p' to print the text to the file")

    while True:
        check, frame = cam.read()

        cv2.imshow('Camera', frame)

        key = cv2.waitKey(1)
        if key == ord("p"):
            cam.release()
            cv2.destroyAllWindows()
            break

    text = pytesseract.image_to_string(frame)
    boxes = pytesseract.image_to_boxes(frame)
    hImg, wImg, _ = frame.shape

    for i in boxes.splitlines():
        # TAKING LETTER'S INFORMATIONS INTO A LIST
        i = i.split()
        print(i)

        # SEPERATING IT'S COORDINATES AND SHAPE
        x, y, width, height = int(i[1]), int(i[2]), int(i[3]), int(i[4])

        # DRAWING THE BOXES
        cv2.rectangle(frame, (x, hImg - y), (width, hImg - height), (0, 0, 255), 1)

    print("\nPress 'q' to print the text into a file.\nPress 'r' to retake the photo")
    cv2.imshow('Photo', frame)

    key = cv2.waitKey(0)
    if key == ord("q"):
        cv2.destroyAllWindows()
        write_to_file(text, "Text_from_camera....")

    elif key == ord("r"):
        cv2.destroyAllWindows()
        cam_to_str()


while True:
    check = int(input("From File 1\nFrom Camera 2\nExit 3\n"))
    if check == 1:
        file_to_str()
    elif check == 2:
        cam_to_str()
    elif check == 3:
        sys.exit()
    else:
        print("Enter a valid number")
