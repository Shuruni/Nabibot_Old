from Tkinter import *
# from PIL import Image, ImageTk
import ttk, tkFont, random, os, sys, csv, time, subprocess, ctypes, datetime

winID = 'NabiGUI' 
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(winID)

top = Tk()
top.attributes("-alpha", 0.0)
top.title("Nabi GUI")
top.wm_iconbitmap(bitmap = "../NabiGUI.ico")

root = Toplevel(top)
root.overrideredirect(1)
root.resizable(0,0)
# root.geometry('1072x726')
root.geometry('1072x726-1924+468')

def onRootLift(event): root.lift()
top.bind("<FocusIn>", onRootLift)

win = Frame(master = root)

curDisplay = "none"
bgColor = "#4d004d"
root.configure(bg = bgColor)
dFont = tkFont.Font(size = 12, family = "Noto Sans")
mFont = tkFont.Font(size = 12, family = "Courier")

CoreClosed = True
OverlayClosed = True

print("yo")

UpStart = time.clock()
UpCurrent = time.clock()

print("end")