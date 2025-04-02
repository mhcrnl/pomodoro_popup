import tkinter as tk
from tkinter import ttk, messagebox
import time

class PomodoroApp:
    def __init__(self, master):
        self.master = master
        master.title("Pomodoro Timer")
        master.geometry("400x300")
        
        # Variabile de configurare
        self.work_time = tk.IntVar(value=25)
        self.short_break = tk.IntVar(value=5)
        self.long_break = tk.IntVar(value=15)
        self.cycles = 0
        self.is_running = False
        self.current_mode = "Work"
        
        # Frame pentru configurare
        config_frame = ttk.LabelFrame(master, text="Settings")
        config_frame.pack(pady=10, padx=20, fill="x")
        
        ttk.Label(config_frame, text="Work (min):").grid(row=0, column=0)
        ttk.Spinbox(config_frame, from_=1, to=60, textvariable=self.work_time, width=5).grid(row=0, column=1)
        
        ttk.Label(config_frame, text="Short Break (min):").grid(row=1, column=0)
        ttk.Spinbox(config_frame, from_=1, to=60, textvariable=self.short_break, width=5).grid(row=1, column=1)
        
        ttk.Label(config_frame, text="Long Break (min):").grid(row=2, column=0)
        ttk.Spinbox(config_frame, from_=1, to=60, textvariable=self.long_break, width=5).grid(row=2, column=1)
        
        # Afișaj timer
        self.time_display = tk.Label(master, text="25:00", font=("Arial", 40))
        self.time_display.pack(pady=20)
        
        # Butoane de control
        btn_frame = tk.Frame(master)
        btn_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(btn_frame, text="Start", command=self.toggle_timer)
        self.start_btn.grid(row=0, column=0, padx=5)
        
        ttk.Button(btn_frame, text="Reset", command=self.reset_timer).grid(row=0, column=1, padx=5)
        
        # Etichetă mod curent
        self.mode_label = tk.Label(master, text="Work Time", fg="red")
        self.mode_label.pack()
        
        # Inițializare timer
        self.reset_timer()
    
    def toggle_timer(self):
        if not self.is_running:
            self.is_running = True
            self.start_btn.config(text="Pause")
            self.update_timer()
        else:
            self.is_running = False
            self.start_btn.config(text="Resume")
    
    def reset_timer(self):
        self.is_running = False
        self.start_btn.config(text="Start")
        self.current_mode = "Work"
        self.time_left = self.work_time.get() * 60
        self.update_display()
        self.mode_label.config(text="Work Time", fg="red")
    
    def update_display(self):
        mins, secs = divmod(self.time_left, 60)
        self.time_display.config(text=f"{mins:02d}:{secs:02d}")
    
    def update_timer(self):
        if self.is_running:
            if self.time_left > 0:
                self.time_left -= 1
                self.update_display()
                self.master.after(1000, self.update_timer)
            else:
                self.is_running = False
                self.start_btn.config(text="Start")
                self.handle_completion()
    
    def handle_completion(self):
        if self.current_mode == "Work":
            self.cycles += 1
            if self.cycles % 4 == 0:
                self.current_mode = "Long Break"
                self.time_left = self.long_break.get() * 60
            else:
                self.current_mode = "Short Break"
                self.time_left = self.short_break.get() * 60
        else:
            self.current_mode = "Work"
            self.time_left = self.work_time.get() * 60
        
        self.mode_label.config(
            text=f"{self.current_mode} Time",
            fg="green" if "Break" in self.current_mode else "red"
        )
        messagebox.showinfo("Timer Complete", f"{self.current_mode} session started!")
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
