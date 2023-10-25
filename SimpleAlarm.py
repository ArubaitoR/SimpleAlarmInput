import tkinter as tk
from tkinter import messagebox
import time
import threading
from pygame import mixer

def set_alarm():
    unit = unit_var.get()
    delay = int(delay_entry.get())
    if unit == "Hours":
        delay *= 3600
    else:
        delay *= 60

    def alarm():
        time.sleep(delay)
        mixer.init()
        mixer.music.load('alarm.mp3')
        mixer.music.play(-1)
        messagebox.showinfo("Alarm", "Time's up!")
        stop_alarm()

    threading.Thread(target=alarm).start()

def stop_alarm():
    mixer.music.stop()

root = tk.Tk()
root.title("Alarm")

unit_var = tk.StringVar(value="Hours")
delay_entry = tk.Entry(root)
delay_entry.pack()

unit_option = tk.OptionMenu(root, unit_var, "Hours", "Minutes")
unit_option.pack()

set_button = tk.Button(root, text="Set", command=set_alarm)
set_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_alarm)
stop_button.pack()

root.mainloop()