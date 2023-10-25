import tkinter as tk
from tkinter import messagebox
import time
import threading
from pygame import mixer

alarm_thread = None
end_time = None
stop_flag = False

def update_label():
    global stop_flag
    if alarm_thread and alarm_thread.is_alive() and not stop_flag:
        remaining = end_time - time.time()
        if remaining <= 0:
            countdown_label.config(text="Time's up")
        else:
            hours, rem = divmod(remaining, 3600)
            minutes, seconds = divmod(rem, 60)
            countdown_label.config(text="{:0>2}:{:0>2}:{:0>2}".format(int(hours), int(minutes), int(seconds)))
    else:
        countdown_label.config(text="Alarm hasn't been set")
    root.after(1000, update_label)

def set_alarm():
    global alarm_thread, end_time, stop_flag
    stop_flag = False
    unit = unit_var.get()
    delay = int(delay_entry.get())
    if unit == "Hours":
        delay *= 3600
    else:
        delay *= 60

    end_time = time.time() + delay

    def alarm():
        for _ in range(delay):
            if stop_flag:
                return
            time.sleep(1)
        mixer.init()
        mixer.music.load('alarm.mp3')
        mixer.music.play(-1)
        messagebox.showinfo("Alarm", "Time's up!")
        stop_alarm()

    alarm_thread = threading.Thread(target=alarm)
    alarm_thread.start()
    alarm_button.config(text="Stop", command=stop_alarm)

def stop_alarm():
    global alarm_thread, stop_flag
    stop_flag = True
    if mixer.get_init():
        mixer.music.stop()
    alarm_button.config(text="Set", command=set_alarm)

root = tk.Tk()
root.title("Alarm")
root.geometry("250x150")  # Adjust the size of the window

frame = tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor='center')

unit_var = tk.StringVar(value="Minutes")
delay_entry = tk.Entry(frame)
delay_entry.pack(anchor='center', pady=10)

unit_option = tk.OptionMenu(frame, unit_var, "Hours", "Minutes")
unit_option.pack(anchor='center')

alarm_button = tk.Button(frame, text="Set", command=set_alarm)
alarm_button.pack(anchor='center')

countdown_label = tk.Label(frame, text="Alarm hasn't been set")
countdown_label.pack(anchor='center', pady=10)

root.after(1000, update_label)

root.mainloop()
