import os
import json
import tkinter as tk
import matplotlib.pyplot as plt
import pytz
from tkinter import ttk, filedialog, messagebox
from tkinter.font import BOLD
from datetime import datetime, timedelta
from collections import defaultdict
from matplotlib import cm

DEFAULT_ACTIVITIES = ['Study', 'Essentials', 'Procrastinating', 'Programming', 'Reading', 'Web-Surfing']
SAVE_DIRECTORY = "saved_sessions"
TIME_FORMAT = '%H:%M'
ELAPSED_TIME_FORMAT = 'Time: {:02}:{:02}:{:02}.{:03}'

class TimeRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title('Time Recorder')
        self.timezone = pytz.timezone('Asia/Seoul')
        self.sessions = []
        self.start_time = None

        self.create_ui_components()
        self.place_ui_components()
        self.update_timer()

    def create_ui_components(self):
        self.activity_var = tk.StringVar()
        self.activity_dropdown = ttk.Combobox(self.root, textvariable=self.activity_var, values=DEFAULT_ACTIVITIES)
        self.timer_label = ttk.Label(self.root, text="00:00:00.000", font=("Arial", 25, BOLD))
        self.date_label = ttk.Label(self.root, text=f"{datetime.now().strftime('%Y-%m-%d')}", font=("Arial", 13, BOLD))
        self.creator = ttk.Label(self.root, text=f"developed by Alex Roh")
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_timer)
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_timer)
        self.save_button = ttk.Button(self.root, text="Save", command=self.save_sessions)
        self.load_button = ttk.Button(self.root, text="Load", command=self.load_sessions)
        self.show_graph_button = ttk.Button(self.root, text="Show Graph", command=self.show_graph)
        self.clear_button = ttk.Button(self.root, text="Clear", command=self.clear_sessions)
        self.listbox = tk.Listbox(self.root, height=10, width=60)

    def place_ui_components(self):
        components_with_grid_options = [
            (self.activity_dropdown, {"row": 0, "column": 0, "pady": 20, "columnspan": 2}),
            (self.timer_label, {"row": 1, "column": 0, "columnspan": 2}),
            (self.start_button, {"row": 2, "column": 0, "pady": 10, "columnspan": 2}),
            (self.stop_button, {"row": 3, "column": 0, "columnspan": 2}),
            (self.date_label, {"row": 4, "column": 0, "padx": 10, "columnspan": 2, "sticky": "se"}),
            (self.listbox, {"row": 5, "column": 0, "pady": 10, "columnspan": 2}),
            (self.save_button, {"row": 6, "column": 0, "columnspan": 2}),
            (self.load_button, {"row": 7, "column": 0, "pady": 10, "columnspan": 2}),
            (self.show_graph_button, {"row": 8, "column": 0, "pady": 20, "columnspan": 2}),
            (self.clear_button, {"row": 9, "column": 0, "pady": 10, "columnspan": 2, "sticky": "n"}),
            (self.creator, {"row": 9, "column": 1, "pady": 10, "sticky": "se"}),
        ]
        
        for component, grid_options in components_with_grid_options:
            component.grid(**grid_options)

    def get_current_datetime(self):
        return datetime.now(self.timezone)

    def start_timer(self):
        if not self.start_time:
            self.start_time = self.get_current_datetime()

    def stop_timer(self):
        if self.start_time:
            stop_time = self.get_current_datetime()
            activity = self.activity_var.get() or "Breathing"
            self.sessions.append({
                'activity': activity,
                'start': self.start_time.timestamp(),
                'end': stop_time.timestamp()
            })
            self.start_time = None
            self.update_activity_list()

    def update_timer(self):
        if self.start_time:
            elapsed = self.get_current_datetime() - self.start_time
            hours, remainder = divmod(elapsed.total_seconds(), 3600)
            minutes, seconds = divmod(remainder, 60)
            milliseconds = int((seconds - int(seconds)) * 1000)
            self.timer_label.config(text=ELAPSED_TIME_FORMAT.format(int(hours), int(minutes), int(seconds), milliseconds))
        else:
            self.timer_label.config(text="Time: 00:00:00.000")
        self.root.after(50, self.update_timer)

    def update_activity_list(self):
        self.listbox.delete(0, tk.END)
        for session in sorted(self.sessions, key=lambda x: x['end'], reverse=True):
            start_time = datetime.fromtimestamp(session['start'], tz=self.timezone).strftime(TIME_FORMAT)
            end_time = datetime.fromtimestamp(session['end'], tz=self.timezone).strftime(TIME_FORMAT)
            elapsed = str(timedelta(seconds=int(session['end'] - session['start'])))
            self.listbox.insert(tk.END, f"{session['activity']}: {start_time} ~ {end_time} ({elapsed})")

    def save_sessions(self):
        timestamp = self.get_current_datetime().strftime('%Y-%m-%d_%H-%M-%S')
        file_path = os.path.join(SAVE_DIRECTORY, f'{timestamp}.json')
        os.makedirs(SAVE_DIRECTORY, exist_ok=True)
        with open(file_path, 'w') as f:
            json.dump(self.sessions, f)
        messagebox.showinfo("Success", f"Sessions saved as '{timestamp}.json'!")

    def load_sessions(self):
        session_file = filedialog.askopenfilename(title="Open Session File", filetypes=[("JSON files", "*.json"), ("All files", "*.*")])
        if session_file:
            try:
                with open(session_file, "r") as file:
                    self.sessions = json.load(file)
                self.update_activity_list()
            except:
                messagebox.showwarning("Error", "Failed to load the session!")

    def clear_sessions(self):
        self.sessions = []
        self.start_time = None
        self.update_activity_list()

    def make_autopct(self, values):
        def my_autopct(pct):
            total_seconds = sum(values)
            hours, remainder = divmod(int(pct / 100 * total_seconds), 3600)
            minutes, seconds = divmod(remainder, 60)
            formatted_time = ""
            if hours > 0:
                formatted_time += f"{hours}h "
            if minutes > 0:
                formatted_time += f"{minutes}m "
            formatted_time += f"{seconds}s"

            return '{p:.2f}%\n({f_time})'.format(p=pct, f_time=formatted_time)
        return my_autopct

    def show_graph(self):
        plt.rcParams['font.family'] ='Malgun Gothic'
        plt.rcParams['axes.unicode_minus'] =False
        
        activity_times = defaultdict(float)
        for session in self.sessions:
            activity_times[session['activity']] += session['end'] - session['start']
        
        labels = list(activity_times.keys())
        values = list(activity_times.values())

        fig, ax = plt.subplots(figsize=(7, 7))
        ax.pie(values, labels=labels, autopct=self.make_autopct(values), startangle=90, colors=cm.Paired.colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.show()

if __name__ == '__main__':
    root = tk.Tk()
    app = TimeRecorder(root)
    root.mainloop()
