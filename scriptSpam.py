import tkinter as tk  # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
import time
import pyautogui as pg

window = tk.Tk()
fr_main = tk.Frame(window)
fr_main.pack()
fr_settings = tk.Frame(fr_main)
fr_settings.grid(row=2,column=0,columnspan=3)
filename = ''
running = True
starting = False
# print(running)
cLine = 0
countDown = 5
secondsBetween = 1
written = 0


def openFile():
    global running, starting, written
    running = True
    starting = True
    global filename
    filename = askopenfilename()  # show an "Open" dialog box and return the path to the selected file
    if filename:
        btn_chooseFile["text"] = filename
        print(filename)
        startLine['state'] = tk.NORMAL
        btn_start['state'] = tk.NORMAL
        written = 0


def copyPasta():
    global file, running, starting, cLine, countDown, written

    btn_start['state'] = tk.DISABLED
    startLine["state"] = tk.DISABLED
    startLine.insert(tk.END, str(cLine))
    lbl_currentLine["text"] = "Current Line: " + str(cLine)

    if running and filename:
        if starting:
            starting = False
            while countDown >= 0:
                lbl_Line['text'] = "Starting in: " + str(countDown)
                for j in range(10):
                    window.update()
                    time.sleep(.10)
                countDown -= 1

        btn_stop['state'] = tk.NORMAL

        file = open(filename, 'r')
        line = file.readlines()
        file.close()

        if cLine < len(line):
            # print(cLine)
            if not (line[cLine].startswith(' ') or line[cLine].startswith('\n')):
                lbl_Line['text'] = line[cLine]
                print(line[cLine], end='')
                pg.write(line[cLine])
                written += 1
                for j in range(10 * secondsBetween):
                    window.update()
                    time.sleep(.1)
            cLine += 1
            copyPasta()
        else:
            running = False
            lbl_Line['text'] = f"Finished all {cLine} Lines\nTotal lines written: {written}"
            lbl_currentLine['text'] = "Current Line: END"
            cLine = 0
            btn_stop['state'] = tk.DISABLED


def stop():
    global running, starting, cLine

    if not btn_stop['state'] == tk.DISABLED:
        if running:
            btn_stop["text"] = "Reset"
            btn_start["text"] = 'Resume'
            running = False
            cLine = 0

        elif not running:
            btn_stop["text"] = "Stop"
            btn_start["text"] = 'Start'
            btn_start['state'] = tk.NORMAL
            running = True
            starting = True
            btn_stop["state"] = tk.DISABLED
            cLine = 0
            lbl_Line['text'] = ''
            window.update()

        print(running)


# All the buttons and labels and stuff:
btn_chooseFile = tk.Button(fr_main, text="No File Chosen", command=openFile, width=30, borderwidth=2)
btn_chooseFile.grid(column=1, row=0, columnspan=3, sticky='nsew')

btn_start = tk.Button(fr_main, text="Start!", command=copyPasta, borderwidth=2, state=tk.DISABLED)
btn_start.grid(column=0, row=3, columnspan=2, sticky='nsew')

lbl_fileName = tk.Label(fr_main, text="Choose File:", anchor='e', relief=tk.SUNKEN, borderwidth=2)
lbl_fileName.grid(column=0, row=0, sticky='nsew')

lbl_currentLine = tk.Label(fr_main, text="Current Line: ", anchor='e', borderwidth=2, width=15)
lbl_currentLine.grid(column=0, row=1, sticky='nsew')

lbl_Line = tk.Label(fr_main, text=" ", width=30, height=2, anchor='n', relief=tk.SUNKEN, borderwidth=2)
lbl_Line.grid(column=1, row=1, columnspan=2, sticky='nsew')

btn_stop = tk.Button(fr_main, text='Stop', command=stop, state=tk.DISABLED)
btn_stop.grid(row=3, column=2, sticky='nsew')

startLine = tk.Entry(fr_settings, width=4, borderwidth=2, relief=tk.SUNKEN)
startLine.grid(row=0, column=1, sticky='nsw')

lbl_startLine = tk.Label(fr_settings, text="Start Line:", anchor='w')
lbl_startLine.grid(row=0, column=0, sticky='nsew')

lbl_countDown = tk.Label(fr_settings, text="Countdown length:", anchor='e')
lbl_countDown.grid(row=1,column=0)

radio2 = tk.Radiobutton()
radio5 = tk.Radiobutton()
radio10 = tk.Radiobutton()



window.mainloop()
