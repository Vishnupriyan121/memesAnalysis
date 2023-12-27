import numpy as np

from tkinter import *
import os
from tkinter import filedialog
import cv2
import time
from tkinter import messagebox


def endprogram():
    print("\nProgram terminated!")
    sys.exit()


def cocr():
    import cv2 as cv

    import easyocr

    import win32com.client as wincl
    speak = wincl.Dispatch("SAPI.SpVoice")
    font = cv.FONT_HERSHEY_SIMPLEX
    reader = easyocr.Reader(['en'])

    cap = cv.VideoCapture(0)

    frame_count = 0
    while (cap.isOpened()):
        hasFrame, frame = cap.read()
        if hasFrame:
            frame_count += 1
            print(frame_count)
            if frame_count % 5 == 0:  # process every other frame to save time
                img = frame
                result = reader.readtext(img)

                # spacer = 100

                for detection in result:
                    text = detection[1]
                    print(text)

                    speak.Speak(text)

            if cv.waitKey(1) & 0xFF == ord('q'):
                break

            cv.imshow('frame', frame)
        else:
            break

    cv.destroyAllWindows()
    cap.release()


def imgtest():
    import_file_path = filedialog.askopenfilename()

    image = cv2.imread(import_file_path)
    print(import_file_path)
    filename = 'Data/Out/Test.jpg'
    cv2.imwrite(filename, image)
    print("After saving image:")
    # result()

    # import_file_path = filedialog.askopenfilename()
    print(import_file_path)
    fnm = os.path.basename(import_file_path)
    print(os.path.basename(import_file_path))

    # file_sucess()

    print("\n*********************\nImage : " + fnm + "\n*********************")
    img = cv2.imread(import_file_path)
    if img is None:
        print('no data')

    img1 = cv2.imread(import_file_path)
    print(img.shape)
    img = cv2.resize(img, ((int)(img.shape[1] / 5), (int)(img.shape[0] / 5)))
    original = img.copy()
    neworiginal = img.copy()
    #cv2.imshow('original', img1)
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)

    img1S = cv2.resize(img1, (960, 540))

    cv2.imshow('Original image', img1S)
    grayS = cv2.resize(gray, (960, 540))
    cv2.imshow('Gray image', grayS)

    dst = cv2.fastNlMeansDenoisingColored(img1, None, 10, 10, 7, 21)
    cv2.imshow("Nosie Removal", dst)
    result()


def result():
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import cv2 as cv

    import easyocr

    import win32com.client as wincl
    speak = wincl.Dispatch("SAPI.SpVoice")
    font = cv.FONT_HERSHEY_SIMPLEX
    reader = easyocr.Reader(['en'])
    filename = 'Data/Out/Test.jpg'
    img = cv2.imread(filename)

    result = reader.readtext(img)

    # spacer = 100
    final_text = ""

    for _, text, __ in result:  # _ = bounding box, text = text and __ = confident level
        final_text += "\n"
        final_text += text
    print(final_text)

    #speak.Speak(final_text)

    sentence = final_text

    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = sid_obj.polarity_scores(sentence)

    string = str(sentiment_dict['neg'] * 100) + "% Negetive"
    # negativeField.insert(10, string)

    string = str(sentiment_dict['neu'] * 100) + "% Neutral"
    # neutralField.insert(10, string)

    string = str(sentiment_dict['pos'] * 100) + "% Positive"
    # positiveField.insert(10, string)

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05:
        string = "Positive"

    elif sentiment_dict['compound'] <= - 0.05:
        string = "Negative"


    else:
        string = "Neutral"

    messagebox.showinfo("Result", "OCR Result : " + str(final_text))
    messagebox.showinfo("Result", "Sentiment Classification Result:" + str(string))


def main_account_screen():
    global main_screen
    main_screen = Tk()
    width = 600
    height = 600
    screen_width = main_screen.winfo_screenwidth()
    screen_height = main_screen.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    main_screen.geometry("%dx%d+%d+%d" % (width, height, x, y))
    main_screen.resizable(0, 0)
    # main_screen.geometry("300x250")
    main_screen.title("Memes DataSet Sentiment Analysis ")

    Label(text="Text Extraction from Memes", width="300", height="5", font=("Calibri", 16)).pack()

    Button(text="Upload Image", font=(
        'Verdana', 15), height="2", width="30", command=imgtest, highlightcolor="black").pack(side=TOP)

    Label(text="").pack()

    main_screen.mainloop()


main_account_screen()
