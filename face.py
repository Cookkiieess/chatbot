import tkinter as tk
import time

class Eye:
    def __init__(self, canvas, x, y, size):
        self.canvas = canvas
        self.original_x = x
        self.x = x
        self.y = y
        self.base_y = y
        self.size = size

        self.mode = "normal"
        self.bounce_dir = 1
        self.look_dir = 1
        self.vibrate_toggle = 1
        self.sleep_animation_step = 0

        # Square-shaped eyes
        self.normal_rect = canvas.create_rectangle(x, y, x+size, y+size, fill='blue', outline='blue', width=6)

        self.happy_arc = canvas.create_arc(x, y+size//2, x+size, y+size+20, start=0, extent=180,
                                           style='arc', outline='cyan', width=6, state='hidden')
        self.sad_arc = canvas.create_arc(x, y+size//2, x+size, y+size+20, start=180, extent=180,
                                         style='arc', outline='lightblue', width=6, state='hidden')
        self.angry_slash = canvas.create_line(x, y, x+size, y+size, fill='red', width=6, state='hidden')
        self.surprise_square = canvas.create_rectangle(x-10, y-10, x+size+10, y+size+10, fill='white', outline='skyblue', width=6, state='hidden')
        self.sleepy_line = canvas.create_line(x, y+size//2, x+size, y+size//2, fill='lightblue', width=6, state='hidden')

    def show_emotion(self, emotion):
        self.mode = emotion
        for item in [self.normal_rect, self.happy_arc, self.sad_arc, self.angry_slash, self.surprise_square, self.sleepy_line]:
            self.canvas.itemconfigure(item, state='hidden')

        if emotion == "normal":
            self.canvas.itemconfigure(self.normal_rect, state='normal')
        elif emotion == "happy":
            self.canvas.itemconfigure(self.happy_arc, state='normal')
        elif emotion == "sad":
            self.canvas.itemconfigure(self.sad_arc, state='normal')
        elif emotion == "angry":
            self.canvas.itemconfigure(self.angry_slash, state='normal')
        elif emotion == "surprised":
            self.canvas.itemconfigure(self.surprise_square, state='normal')
        elif emotion == "sleepy":
            self.canvas.itemconfigure(self.sleepy_line, state='normal')

    def animate(self):
        if self.mode == "happy":
            self.y += self.bounce_dir * 1.5
            if self.y < self.base_y - 5 or self.y > self.base_y + 5:
                self.bounce_dir *= -1
            self.canvas.coords(self.happy_arc, self.x, self.y+self.size//2, self.x+self.size, self.y+self.size+20)

        elif self.mode == "normal":
            self.x += self.look_dir * 0.8
            if self.x > self.original_x + 10 or self.x < self.original_x - 10:
                self.look_dir *= -1
            self.canvas.coords(self.normal_rect, self.x, self.y, self.x+self.size, self.y+self.size)

        elif self.mode == "sad":
            self.y += self.bounce_dir * 0.5
            if self.y < self.base_y - 3 or self.y > self.base_y + 3:
                self.bounce_dir *= -1
            self.canvas.coords(self.sad_arc, self.x, self.y+self.size//2, self.x+self.size, self.y+self.size+20)

        elif self.mode == "angry":
            dx = 1 * self.vibrate_toggle
            self.canvas.move(self.angry_slash, dx, 0)
            self.vibrate_toggle *= -1

        elif self.mode == "surprised":
            pulse = 1.5 * self.vibrate_toggle
            self.canvas.coords(self.surprise_square,
                self.x - 10 - pulse, self.y - 10 - pulse,
                self.x + self.size + 10 + pulse, self.y + self.size + 10 + pulse)
            self.vibrate_toggle *= -1

        elif self.mode == "sleepy":
            max_step = 20
            if self.sleep_animation_step < max_step:
                offset = self.sleep_animation_step
                self.canvas.coords(self.sleepy_line, self.x+offset, self.y+self.size//2, self.x+self.size-offset, self.y+self.size//2)
                self.sleep_animation_step += 1
            else:
                self.canvas.coords(self.sleepy_line, self.x, self.y+self.size//2, self.x+self.size, self.y+self.size//2)

class EmotionBotEyesApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Emotion Bot Eyes")
        self.root.configure(bg='black')
        self.root.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(self.root, bg='black', highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        size = 100
        y_pos = screen_height//3
        x_offset = 200

        self.eyes = [
            Eye(self.canvas, screen_width//2 - x_offset, y_pos, size),
            Eye(self.canvas, screen_width//2 + x_offset - size, y_pos, size)
        ]

        self.label = tk.Label(self.root, text="How are you feeling today?", fg="white", bg="black", font=("Arial", 20))
        self.label.pack(pady=(10, 0))

        self.input_field = tk.Entry(self.root, font=("Arial", 18), width=40)
        self.input_field.pack(pady=20)
        self.input_field.bind("<Return>", self.check_emotion)
        self.input_field.bind("<Key>", self.reset_idle_timer)

        self.root.bind("<Motion>", self.reset_idle_timer)

        self.last_activity_time = time.time()
        self.current_emotion = "normal"

        self.animate()

    def reset_idle_timer(self, event=None):
        was_sleeping = self.current_emotion == "sleepy"
        self.last_activity_time = time.time()
        if was_sleeping:
            self.set_emotion("surprised")
            self.root.after(1000, lambda: self.set_emotion("normal"))
        elif self.current_emotion == "sleepy":
            self.set_emotion("normal")

    def check_emotion(self, event=None):
        text = self.input_field.get().lower()

        if any(word in text for word in ["happy", "great", "awesome", "good"]):
            emotion = "happy"
        elif any(word in text for word in ["sad", "down", "blue"]):
            emotion = "sad"
        elif any(word in text for word in ["angry", "mad", "furious"]):
            emotion = "angry"
        elif any(word in text for word in ["wow", "surprised", "shocked"]):
            emotion = "surprised"
        else:
            emotion = "normal"

        self.set_emotion(emotion)

    def set_emotion(self, emotion):
        self.current_emotion = emotion
        for eye in self.eyes:
            eye.show_emotion(emotion)
            if emotion == "sleepy":
                eye.sleep_animation_step = 0

    def animate(self):
        if time.time() - self.last_activity_time > 10:
            if self.current_emotion != "sleepy":
                self.set_emotion("sleepy")

        for eye in self.eyes:
            eye.animate()
        self.root.after(30, self.animate)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    EmotionBotEyesApp().run()
