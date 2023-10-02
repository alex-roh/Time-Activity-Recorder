import json
import tkinter as tk
import matplotlib.pyplot as plt
import pytz
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
from collections import defaultdict
from matplotlib import cm

class TimeRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title('Time Recorder')

        # Set timezone to KST
        self.timezone = pytz.timezone('Asia/Seoul')

        # Internal state
        self.sessions = []
        self.start_time = None

        # GUI Components
        default_activities = ['Study', 'Essentials', 'Procrastinating', 'Programming', 'Reading', 'Web-Surfing']
        self.activity_var = tk.StringVar()
        self.activity_dropdown = ttk.Combobox(root, textvariable=self.activity_var, values=default_activities)
        self.activity_dropdown.pack(pady=20)

        self.timer_label = ttk.Label(root, text="Time: 00:00:00.000")
        self.timer_label.pack()

        # self.start_img = tk.PhotoImage(file="start.png")
        # self.stop_img = tk.PhotoImage(file="stop.png")

        self.start_button = ttk.Button(root, text="Start", command=self.start_timer)
        self.start_button.pack()

        self.stop_button = ttk.Button(root, text="Stop", command=self.stop_timer)
        self.stop_button.pack(pady=20)

        self.date_label = ttk.Label(root, text=f"Today's Date: {datetime.now().strftime('%Y-%m-%d')}")
        self.date_label.pack()

        self.listbox = tk.Listbox(root, height=10, width=60)
        self.listbox.pack(pady=20)

        self.save_button = ttk.Button(root, text="Save", command=self.save_sessions)
        self.save_button.pack()

        self.load_button = ttk.Button(root, text="Load", command=self.load_sessions)
        self.load_button.pack(pady=20)

        self.show_graph_button = ttk.Button(root, text="Show Graph", command=self.show_graph)
        self.show_graph_button.pack(pady=20)

        # Update timer method
        self.update_timer()

    def get_current_datetime(self):
        return datetime.now(self.timezone)

    def start_timer(self):
        if not self.start_time:
            self.start_time = self.get_current_datetime()

    def stop_timer(self):
        if self.start_time:
            stop_time = self.get_current_datetime()
            activity = self.activity_var.get()
            if activity == '':
                activity = "Breathing"
            session = {
                'activity': activity,
                'start': self.start_time.timestamp(),
                'end': stop_time.timestamp()
            }
            self.sessions.append(session)
            self.start_time = None
            self.update_activity_list()

    def update_timer(self):
        if self.start_time:
            elapsed = self.get_current_datetime() - self.start_time
            time_str = str(timedelta(seconds=int(elapsed.total_seconds())))
            self.timer_label.config(text=f"Time: {time_str}")
        else:
            self.timer_label.config(text="Time: 00:00:00:00.000")
        self.root.after(50, self.update_timer)

    def update_activity_list(self):
        self.listbox.delete(0, tk.END)
        sorted_sessions = sorted(self.sessions, key=lambda x: x['end'], reverse=True)
        for session in sorted_sessions:
            start_time = datetime.fromtimestamp(session['start'], tz=self.timezone).strftime('%H:%M')
            end_time = datetime.fromtimestamp(session['end'], tz=self.timezone).strftime('%H:%M')
            elapsed = str(timedelta(seconds=int(session['end'] - session['start'])))
            self.listbox.insert(tk.END, f"{session['activity']}: {start_time} ~ {end_time} ({elapsed})")

    def save_sessions(self):
        timestamp = self.get_current_datetime().strftime('%Y-%m-%d_%H-%M-%S')
        with open(f'{timestamp}.json', 'w') as f:
            json.dump(self.sessions, f)
        messagebox.showinfo("Success", f"Sessions saved as '{timestamp}.json'!")

    def load_sessions(self):
        session_file = filedialog.askopenfilename(
            title="Open Session File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if session_file:
            try:
                with open(session_file, "r") as file:
                    self.sessions = json.load(file)
                self.update_activity_list()
            except Exception as e:
                messagebox.showwarning("Error", "No sessions found to load!")

    def make_autopct(self, values):
        def my_autopct(pct):
            total = sum(values)
            val = int(round(pct*total/100.0))
            return '{p:.2f}%  ({v:d})'.format(p=pct,v=val)
        return my_autopct

    def show_graph(self):
        activity_time = defaultdict(int)
        for session in self.sessions:
            activity_time[session['activity']] += (session['end'] - session['start']) / 60 # minutes base
        activities = list(activity_time.keys())
        times = list(activity_time.values())
        colors = cm.rainbow([x / len(activities) for x in range(len(activities))])
        plt.pie(times, labels=activities, colors=colors, autopct=self.make_autopct(times))
        plt.title('Time spent on activities')
        plt.show()

if __name__ == '__main__':
    root = tk.Tk()
    app = TimeRecorder(root)
    root.mainloop()