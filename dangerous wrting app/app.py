import tkinter as tk
from tkinter import ttk


class DangerousWritingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dangerous Writing App")
        self.root.geometry("600x400")

        # Timer settings
        self.timer_duration = 5000  # 5 seconds
        self.timer = None
        self.elapsed_time = 0

        # Set up the main frame
        self.main_frame = ttk.Frame(self.root, padding="10 10 10 10")
        self.main_frame.pack(expand=True, fill='both')

        # Set up the text area
        self.text_area = tk.Text(self.main_frame, wrap='word', font=('Helvetica', 14), undo=True, bg="#F9F9F9", fg="#333")
        self.text_area.pack(expand=True, fill='both', padx=5, pady=5)
        self.text_area.bind('<Key>', self.reset_timer)

        # Timer label
        self.timer_label = ttk.Label(self.main_frame, text="Time Elapsed: 0 sec", font=('Helvetica', 10, 'italic'))
        self.timer_label.pack(side='top', anchor='w')

        # Status label
        self.status_label = ttk.Label(self.main_frame, text="Keep typing... or else!", font=('Helvetica', 12, 'bold'))
        self.status_label.pack(side='bottom', pady=(10, 0))

        # Start the timer
        self.reset_timer()

    def reset_timer(self, event=None):
        if self.timer is not None:
            self.root.after_cancel(self.timer)
        self.elapsed_time = 0
        self.update_timer()
        self.timer = self.root.after(self.timer_duration, self.clear_text)

    def update_timer(self):
        self.elapsed_time += 1
        self.timer_label.config(text=f"Time Elapsed: {self.elapsed_time} sec")
        if self.timer is not None:
            self.root.after(1000, self.update_timer)

    def clear_text(self):
        self.text_area.delete(1.0, tk.END)
        self.status_label.config(text="You stopped! Everything is gone...", foreground="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = DangerousWritingApp(root)
    root.mainloop()
