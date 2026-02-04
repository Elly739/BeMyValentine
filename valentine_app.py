import tkinter as tk
import random
import winsound

# ------------------ SETUP WINDOW ------------------
root = tk.Tk()
root.title("💌 Be My Valentine? 💌")
root.geometry("500x400")
root.config(bg="#FFC0CB")

# FULL SCREEN MODE
root.attributes("-fullscreen", True)  # Opens full-screen
root.bind("<Escape>", lambda e: root.destroy())  # ESC to exit

# PLAY START CHIME
winsound.MessageBeep(winsound.MB_OK)  # default Windows chime
# Or use a custom sound: winsound.PlaySound("chime.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)

# ------------------ MAIN LABEL ------------------
label = tk.Label(root, text="Will you be my Valentine?", font=("Comic Sans MS", 20, "bold"), bg="#FFC0CB", fg="#800020")
label.pack(pady=40)

# ------------------ YES BUTTON ------------------
yes_size = 14
size_direction = 1

def pulse_yes():
    global yes_size, size_direction
    yes_size += size_direction
    if yes_size > 18 or yes_size < 14:
        size_direction *= -1
    yes_button.config(font=("Comic Sans MS", yes_size, "bold"))
    root.after(150, pulse_yes)

def yes_click():
    label.config(text="💖 Yay! You said Yes! 💖", fg="#FF1493")
    yes_button.config(bg="#FF69B4")
    no_button.place_forget()
    start_confetti()
    create_sparkles()
    heart_fireworks()  # <-- adds the fireworks


yes_button = tk.Button(root, text="Yes", command=yes_click, bg="#FF69B4", fg="white", width=8)
yes_button.place(x=100, y=300)
pulse_yes()

# ------------------ NO BUTTON ------------------
def move_no(event):
    new_x = random.randint(0, 400)
    new_y = random.randint(100, 300)
    no_button.place(x=new_x, y=new_y)

no_button = tk.Button(root, text="No", bg="#C0C0C0", fg="white", width=8)
no_button.place(x=300, y=300)
no_button.bind("<Enter>", move_no)

# ------------------ FLOATING HEARTS ------------------
hearts = ["💖", "💘", "💕", "💞"]
heart_labels = []

for i in range(25):
    heart = tk.Label(root, text=random.choice(hearts), font=("Arial", random.randint(12, 24)), bg="#FFC0CB")
    heart.x = random.randint(0, 450)
    heart.y = random.randint(0, 350)
    heart.dx = random.choice([-1,1])
    heart.dy = random.choice([-1,-2,-3])
    heart.place(x=heart.x, y=heart.y)
    heart_labels.append(heart)

def animate_hearts():
    for heart in heart_labels:
        heart.x += heart.dx
        heart.y += heart.dy
        if heart.y < -30:
            heart.y = 400
            heart.x = random.randint(0, 450)
        if heart.x < 0 or heart.x > 450:
            heart.dx *= -1
        heart.place(x=heart.x, y=heart.y)
    root.after(50, animate_hearts)

animate_hearts()

# ------------------ CONFETTI WITH RANDOM COLORS ------------------
confetti_labels = []

def start_confetti():
    for i in range(40):
        confetti = tk.Label(root, text=random.choice(hearts),
                            font=("Arial", random.randint(12,20)), 
                            bg="#FFC0CB", 
                            fg=random.choice(["#FFD700","#FF69B4","#FFB6C1","#FF4500","#FF1493"]))
        confetti.x = random.randint(0, 450)
        confetti.y = 0
        confetti.dx = random.randint(-3,3)
        confetti.dy = random.randint(3,8)
        confetti.place(x=confetti.x, y=confetti.y)
        confetti_labels.append(confetti)
    animate_confetti()

def animate_confetti():
    still_confetti = []
    for c in confetti_labels:
        c.x += c.dx
        c.y += c.dy
        # Change color randomly as it falls
        c.config(fg=random.choice(["#FFD700","#FF69B4","#FFB6C1","#FF4500","#FF1493"]))
        if c.y < 400:
            c.place(x=c.x, y=c.y)
            still_confetti.append(c)
        else:
            c.place_forget()
    if still_confetti:
        root.after(50, animate_confetti)
    else:
        show_surprise()

# ------------------ HEART FIREWORKS ON YES ------------------
def heart_fireworks():
    fireworks = []
    for _ in range(50):
        heart = tk.Label(root, text=random.choice(hearts),
                         font=("Arial", random.randint(12,20)),
                         bg="#FFC0CB",
                         fg=random.choice(["#FFD700","#FF69B4","#FFB6C1","#FF4500","#FF1493"]))
        # Start from center of screen
        heart.x = root.winfo_width() // 2
        heart.y = root.winfo_height() // 2
        # Random explosion direction
        heart.dx = random.randint(-10,10)
        heart.dy = random.randint(-10,10)
        heart.place(x=heart.x, y=heart.y)
        fireworks.append(heart)
    
    def animate_fireworks():
        still_fireworks = []
        for f in fireworks:
            f.x += f.dx
            f.y += f.dy
            f.place(x=f.x, y=f.y)
            f.config(fg=random.choice(["#FFD700","#FF69B4","#FFB6C1","#FF4500","#FF1493"]))
            # Remove if out of screen
            if 0 <= f.x <= root.winfo_width() and 0 <= f.y <= root.winfo_height():
                still_fireworks.append(f)
            else:
                f.place_forget()
        if still_fireworks:
            root.after(50, animate_fireworks)
    
    animate_fireworks()


# ------------------ SPARKLES ------------------
sparkles = []
def create_sparkles():
    for _ in range(30):
        sparkle = tk.Label(root, text="✨", font=("Arial", random.randint(10,16)), bg="#FFC0CB", fg=random.choice(["#FFD700","#FF69B4","#FFB6C1"]))
        sparkle.x = random.randint(0, 480)
        sparkle.y = random.randint(0, 380)
        sparkle.place(x=sparkle.x, y=sparkle.y)
        sparkles.append(sparkle)
    animate_sparkles()

def animate_sparkles():
    for s in sparkles:
        s.place_forget() if random.random() > 0.5 else s.place(x=s.x, y=s.y)
    root.after(200, animate_sparkles)

# ------------------ SURPRISE POPUP ------------------
def show_surprise():
    popup = tk.Toplevel(root)
    popup.title("💌 Surprise!")
    popup.geometry("300x200")
    popup.config(bg="#FFB6C1")
    msg = tk.Label(popup, text="You made my day! 💖", font=("Comic Sans MS", 18, "bold"), bg="#FFB6C1", fg="#800020")
    msg.pack(expand=True)
    
    alpha = 0.0
    popup.attributes("-alpha", alpha)
    
    def fade_in():
        nonlocal alpha
        if alpha < 1.0:
            alpha += 0.05
            popup.attributes("-alpha", alpha)
            popup.after(50, fade_in)
        else:
            popup.after(2000, fade_out)
    
    def fade_out():
        nonlocal alpha
        if alpha > 0:
            alpha -= 0.05
            popup.attributes("-alpha", alpha)
            popup.after(50, fade_out)
        else:
            popup.destroy()
    
    fade_in()

# ------------------ HEART TRAIL ------------------
trail_hearts = []
def create_heart_trail(event):
    heart = tk.Label(root, text=random.choice(hearts), font=("Arial", random.randint(10,16)), bg="#FFC0CB")
    heart.place(x=event.x, y=event.y)
    trail_hearts.append(heart)
    root.after(500, lambda: heart.destroy())

root.bind("<Motion>", create_heart_trail)

# ------------------ RUN ------------------
root.mainloop()
