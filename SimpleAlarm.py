import tkinter as tk
from tkinter import messagebox
from datetime import timedelta, datetime
from pygame import mixer
import alarmstring
import base64
import tempfile

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.end_time = None
        self.alarm_set = False
        self.initialize_ui()
        mixer.init()

    def initialize_ui(self):
        self.root.title("Alarm")
        self.root.geometry("250x120")

        self.input_frame = tk.Frame(self.root)
        self.input_frame.pack(pady=(20, 5))

        self.hour_entry = self.create_entry(self.input_frame, "Hours", 8)
        self.minute_entry = self.create_entry(self.input_frame, "Minutes", 8)
        self.second_entry = self.create_entry(self.input_frame, "Seconds", 8)

        self.button_label_frame = tk.Frame(self.root)
        self.button_label_frame.pack(pady=5)

        self.alarm_button = tk.Button(self.button_label_frame, text="Set", command=self.set_alarm)
        self.alarm_button.pack(anchor='center')

        self.countdown_label = tk.Label(self.button_label_frame, text="Alarm hasn't been set")
        self.countdown_label.pack(anchor='center', pady=5)

        self.update_label()

    def create_entry(self, parent, placeholder, width):
        entry = tk.Entry(parent, width=width, justify='center')
        entry.insert(0, placeholder)
        entry.config(fg='grey')
        entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, entry, placeholder))
        entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, entry, placeholder))
        entry.pack(side='left', padx=5)
        return entry

    def clear_placeholder(self, event, entry, default_text):
        if entry.get() == default_text:
            entry.delete(0, tk.END)
        entry.config(fg='black')

    def add_placeholder(self, event, entry, default_text):
        if not entry.get():
            entry.insert(0, default_text)
            entry.config(fg='grey')

    def update_label(self):
        if self.alarm_set:
            remaining = (self.end_time - datetime.now()).total_seconds()
            if remaining <= 0:
                self.countdown_label.config(text="Time's up")
                self.alarm_set = False
            else:
                countdown_text = str(timedelta(seconds=remaining)).split('.')[0]
                self.countdown_label.config(text=countdown_text)
        else:
            self.countdown_label.config(text="Alarm hasn't been set")
        self.root.after(1000, self.update_label)

    def set_alarm(self):
        hours = int(self.hour_entry.get() if self.hour_entry.get() and self.hour_entry.get() != "Hours" else 0)
        minutes = int(self.minute_entry.get() if self.minute_entry.get() and self.minute_entry.get() != "Minutes" else 0)
        seconds = int(self.second_entry.get() if self.second_entry.get() and self.second_entry.get() != "Seconds" else 0)
        delay = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        self.end_time = datetime.now() + delay
        self.alarm_set = True
        self.alarm_button.config(text="Stop", command=self.stop_alarm)
        self.root.after(int(delay.total_seconds() * 1000), self.play_alarm)

    def play_alarm(self):
        if self.alarm_set:
            alarm_bytes = base64.b64decode(alarmstring.encoded_string)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio_file:
                temp_audio_file.write(alarm_bytes)
            mixer.music.load(temp_audio_file.name)
            mixer.music.play(-1)
            messagebox.showinfo("Alarm", "Time's up!")
            self.stop_alarm()

    def stop_alarm(self):
        self.alarm_set = False
        if mixer.get_init():
            mixer.music.stop()
        self.alarm_button.config(text="Set", command=self.set_alarm)

if __name__ == "__main__":
    root = tk.Tk()
    alarm_clock = AlarmClock(root)
    root.mainloop()
