import tkinter as tk
from tkinter import font as tkfont
from PIL import Image, ImageTk
import pygame

class ChessClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Battletimer")
        self.root.configure(bg="#E7ECEF")
        self.root.state('zoomed')  # Use maximized window with window controls

        # Custom Font
        self.custom_font = tkfont.Font(family="Nunito Sans", size=60, weight="bold")  # Increased font size

        # Initialize colors and timer state
        self.on_color = "#9CEC5B"
        self.off_color = "#696969"
        self.bg_color = "#E7ECEF"
        self.text_on_color = "white"
        self.text_off_color = "black"
        self.timer_running = False
        self.initial_left_time = 10 * 60
        self.initial_right_time = 10 * 60
        self.left_time_remaining = self.initial_left_time
        self.right_time_remaining = self.initial_right_time
        self.current_side = "right"  # Start with the right side
        self.increment_left = 0
        self.increment_right = 0

        # Initialize pygame for sound
        pygame.mixer.init()

        # Set grid weight to make the panels expand
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)

        # Left Panel
        self.left_panel = tk.Frame(root, bg=self.off_color)
        self.left_panel.grid(row=0, column=0, sticky="nsew")

        # Right Panel
        self.right_panel = tk.Frame(root, bg=self.on_color)
        self.right_panel.grid(row=0, column=2, sticky="nsew")

        # Timer Display (Left)
        self.left_time = tk.Label(self.left_panel, text=self.format_time(self.left_time_remaining),
                                  font=self.custom_font, fg=self.text_off_color, bg=self.off_color)
        self.left_time.pack(expand=True, fill="both")

        # Timer Display (Right)
        self.right_time = tk.Label(self.right_panel, text=self.format_time(self.right_time_remaining),
                                   font=self.custom_font, fg=self.text_on_color, bg=self.on_color)
        self.right_time.pack(expand=True, fill="both")

        # Controls (Center)
        self.center_controls = tk.Frame(root, bg=self.bg_color)
        self.center_controls.grid(row=0, column=1, sticky="nsew")

        # Load and scale icons
        pause_image = Image.open("pause_icon.png").resize((90, 90), Image.LANCZOS)
        restart_image = Image.open("restart_icon.png").resize((100, 100), Image.LANCZOS)
        clock_image = Image.open("clock_icon.png").resize((100, 100), Image.LANCZOS)

        self.pause_icon = ImageTk.PhotoImage(pause_image)
        self.restart_icon = ImageTk.PhotoImage(restart_image)
        self.clock_icon = ImageTk.PhotoImage(clock_image)

        # Pause Button
        self.pause_button = tk.Button(self.center_controls, image=self.pause_icon, command=self.toggle_timer,
                                      relief="flat", bg=self.bg_color, borderwidth=0, highlightthickness=0)
        self.pause_button.pack(pady=20)

        # Replay Button
        self.replay_button = tk.Button(self.center_controls, image=self.restart_icon, command=self.reset_timers,
                                       relief="flat", bg=self.bg_color, borderwidth=0, highlightthickness=0)
        self.replay_button.pack(pady=20)

        # Add Increment Button
        self.increment_button = tk.Button(self.center_controls, image=self.clock_icon,
                                          command=self.set_increment, relief="flat", bg=self.bg_color,
                                          borderwidth=0, highlightthickness=0)
        self.increment_button.pack(pady=20)

        # Bind space bar to color inversion method
        self.root.bind("<space>", self.toggle_colors)

        # Start the timer update loop
        self.update_timer()

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}"

    def update_timer(self):
        if self.timer_running:
            if self.current_side == "left" and self.left_time_remaining > 0:
                self.left_time_remaining -= 1
                self.left_time.config(text=self.format_time(self.left_time_remaining))
                if self.left_time_remaining == 0:
                    self.left_time.config(fg="red")
            elif self.current_side == "right" and self.right_time_remaining > 0:
                self.right_time_remaining -= 1
                self.right_time.config(text=self.format_time(self.right_time_remaining))
                if self.right_time_remaining == 0:
                    self.right_time.config(fg="red")
            
            print(f"Timer update - Current side: {self.current_side}")
            print(f"Timer update - Left time: {self.left_time_remaining}, Right time: {self.right_time_remaining}")

        self.root.after(1000, self.update_timer)

    def toggle_colors(self, event=None):
        # Play sound
        pygame.mixer.music.load(r"click_sound.mp3")
        pygame.mixer.music.play()

        print(f"Before toggle - Current side: {self.current_side}")
        print(f"Before toggle - Left time: {self.left_time_remaining}, Right time: {self.right_time_remaining}")

        # Apply the increment to the side that's about to start its turn
        if self.current_side == "left":
            self.right_time_remaining += self.increment_right
            print(f"Applied right increment: {self.increment_right}")
            self.left_panel.configure(bg=self.off_color)
            self.right_panel.configure(bg=self.on_color)
            self.left_time.configure(bg=self.off_color, fg=self.text_off_color)
            self.right_time.configure(bg=self.on_color, fg=self.text_on_color)
            self.current_side = "right"
        else:  # right side
            self.left_time_remaining += self.increment_left
            print(f"Applied left increment: {self.increment_left}")
            self.left_panel.configure(bg=self.on_color)
            self.right_panel.configure(bg=self.off_color)
            self.left_time.configure(bg=self.on_color, fg=self.text_on_color)
            self.right_time.configure(bg=self.off_color, fg=self.text_off_color)
            self.current_side = "left"

        print(f"After toggle - Current side: {self.current_side}")
        print(f"After toggle - Left time: {self.left_time_remaining}, Right time: {self.right_time_remaining}")

        # Start the timer on space press
        self.timer_running = True

    def toggle_timer(self):
        self.timer_running = not self.timer_running

    def reset_timers(self):
        self.increment_left = 0
        self.increment_right = 0
        self.open_window("replay")

    def set_increment(self):
        self.open_window("increment")
        print(f"Current increments - Left: {self.increment_left}, Right: {self.increment_right}")

    def open_window(self, window_type):
        new_window = tk.Toplevel(self.root)
        new_window.title("Input Window")
        new_window.configure(bg="#E7ECEF")  # Match the main window background
        new_window.geometry("400x200")  # Smaller window size

        if window_type == "increment":
            label_text = "Enter increment (seconds):"
        elif window_type == "replay":
            label_text = "Enter new time for both players (MM:SS):"
        else:
            return  # Invalid type

        label = tk.Label(new_window, text=label_text, bg="#E7ECEF", fg="black", font=("Nunito Sans", 14))  # Clear font and color
        label.pack(pady=15)

        entry = tk.Entry(new_window, font=("Nunito Sans", 14))  # Match font size
        entry.pack(pady=10)

        submit_button = tk.Button(new_window, text="Submit",
                                  command=lambda: self.handle_submission(entry.get(), window_type, new_window),
                                  relief="flat", bg="white", fg="black", borderwidth=0, highlightthickness=0)
        submit_button.pack(pady=15)

    def handle_submission(self, value, window_type, window):
        try:
            if window_type == "increment":
                increment = int(value)
                self.increment_left = increment
                self.increment_right = increment
                print(f"Set increments - Left: {self.increment_left}, Right: {self.increment_right}")
            elif window_type == "replay":
                minutes, seconds = map(int, value.split(":"))
                total_seconds = minutes * 60 + seconds
                self.initial_left_time = total_seconds
                self.initial_right_time = total_seconds
                self.left_time_remaining = total_seconds
                self.right_time_remaining = total_seconds
                self.left_time.config(text=self.format_time(self.left_time_remaining), fg=self.text_on_color)
                self.right_time.config(text=self.format_time(self.right_time_remaining), fg=self.text_off_color)
            else:
                print("Invalid window type.")
            
        except ValueError:
            print("Invalid input. Please enter a valid time or increment.")
        
        window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessClock(root)
    root.mainloop()