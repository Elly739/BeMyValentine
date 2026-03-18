import random
import tkinter as tk
import winsound


BG_TOP = "#fff5f8"
BG_BOTTOM = "#ffd8e5"
CARD_BG = "#fffafc"
CARD_BORDER = "#f5abc1"
PRIMARY = "#eb5b8a"
PRIMARY_HOVER = "#d94879"
SECONDARY = "#9a5673"
TEXT_MAIN = "#5e2c41"
TEXT_SOFT = "#8e6274"
SHADOW = "#f7c4d5"
HEARTS = ["❤", "💖", "💕", "💘"]
CONFETTI_COLORS = ["#ff6f91", "#ff8fab", "#f7c66f", "#ff9a8b", "#ff4d6d"]


root = tk.Tk()
root.title("Be My Valentine?")
root.geometry("1100x720")
root.minsize(900, 620)
root.configure(bg=BG_TOP)
root.bind("<Escape>", lambda _event: root.destroy())

winsound.MessageBeep(winsound.MB_OK)

background = tk.Canvas(root, highlightthickness=0, bd=0)
background.place(relx=0, rely=0, relwidth=1, relheight=1)

shadow_frame = tk.Frame(root, bg=SHADOW)
card_frame = tk.Frame(root, bg=CARD_BG, highlightbackground=CARD_BORDER, highlightthickness=2)
content_frame = tk.Frame(card_frame, bg=CARD_BG)
content_frame.pack(fill="both", expand=True, padx=36, pady=32)

background_hearts = []
trail_items = []
celebration_items = []
accepted = False
yes_font_size = 18
yes_direction = 1
no_position_index = 0
no_positions = []


def create_gradient(width: int, height: int) -> None:
    background.delete("gradient")
    r1, g1, b1 = root.winfo_rgb(BG_TOP)
    r2, g2, b2 = root.winfo_rgb(BG_BOTTOM)
    steps = max(height, 1)
    for i in range(steps):
        nr = int(r1 + (r2 - r1) * i / steps) // 256
        ng = int(g1 + (g2 - g1) * i / steps) // 256
        nb = int(b1 + (b2 - b1) * i / steps) // 256
        color = f"#{nr:02x}{ng:02x}{nb:02x}"
        background.create_line(0, i, width, i, fill=color, tags="gradient")
    background.tag_lower("gradient")


def seed_background_hearts(width: int, height: int) -> None:
    global background_hearts
    for item in background_hearts:
        background.delete(item["id"])
    background_hearts = []

    for _ in range(24):
        x = random.randint(20, max(21, width - 20))
        y = random.randint(20, max(21, height - 20))
        item_id = background.create_text(
            x,
            y,
            text=random.choice(HEARTS),
            font=("Segoe UI Emoji", random.randint(18, 32)),
            fill=random.choice(["#ffc2d6", "#ffb3c9", "#f8a8c3"]),
        )
        background_hearts.append(
            {
                "id": item_id,
                "x": x,
                "y": y,
                "dx": random.uniform(-1.2, 1.2),
                "dy": random.uniform(-1.8, -0.4),
            }
        )


def animate_background_hearts() -> None:
    width = max(root.winfo_width(), 1)
    height = max(root.winfo_height(), 1)

    for item in background_hearts:
        item["x"] += item["dx"]
        item["y"] += item["dy"]
        if item["y"] < -40:
            item["y"] = height + 20
            item["x"] = random.randint(20, max(21, width - 20))
        if item["x"] < -20 or item["x"] > width + 20:
            item["dx"] *= -1
        background.coords(item["id"], item["x"], item["y"])

    root.after(40, animate_background_hearts)


def create_heart_trail(event) -> None:
    item_id = background.create_text(
        event.x,
        event.y,
        text=random.choice(HEARTS),
        font=("Segoe UI Emoji", random.randint(10, 16)),
        fill=random.choice(["#ff9fbb", "#ffb8cd", "#ffc7d7"]),
    )
    trail_items.append(item_id)
    if len(trail_items) > 30:
        old = trail_items.pop(0)
        background.delete(old)
    root.after(450, lambda current=item_id: background.delete(current))


def layout_shell() -> None:
    width = root.winfo_width()
    height = root.winfo_height()
    card_width = min(720, width - 120)
    card_height = 440
    card_x = (width - card_width) // 2
    card_y = (height - card_height) // 2

    shadow_frame.place(x=card_x + 10, y=card_y + 12, width=card_width, height=card_height)
    card_frame.place(x=card_x, y=card_y, width=card_width, height=card_height)
    shadow_frame.lift()
    card_frame.lift()


def romantic_no_positions() -> list[tuple[int, int]]:
    width = root.winfo_width()
    height = root.winfo_height()
    return [
        (width // 2 + 150, height // 2 + 70),
        (width // 2 - 290, height // 2 + 115),
        (width // 2 + 250, height // 2 - 70),
        (width // 2 - 60, height // 2 + 175),
        (width // 2 + 310, height // 2 + 145),
    ]


def place_no_button(initial: bool = False) -> None:
    global no_positions, no_position_index
    if accepted:
        no_button.place_forget()
        return

    no_positions = romantic_no_positions()
    if initial:
        no_position_index = 0
    x, y = no_positions[no_position_index]
    no_button.place(x=x, y=y, width=92, height=52)
    no_button.lift()


def move_no_button() -> None:
    global no_position_index
    if accepted:
        return
    no_position_index = (no_position_index + 1) % len(no_positions)
    place_no_button()
    status_label.config(text="That answer is feeling a little shy today.")


def pulse_yes() -> None:
    global yes_font_size, yes_direction
    if accepted:
        return
    yes_font_size += yes_direction
    if yes_font_size >= 21 or yes_font_size <= 18:
        yes_direction *= -1
    yes_button.config(font=("Segoe UI", yes_font_size, "bold"))
    root.after(140, pulse_yes)


def clear_content() -> None:
    for child in content_frame.winfo_children():
        child.destroy()


def animate_celebration() -> None:
    active = []
    for item in celebration_items:
        item["x"] += item["dx"]
        item["y"] += item["dy"]
        item["life"] -= 1
        if item["life"] > 0:
            background.coords(item["id"], item["x"], item["y"])
            background.itemconfig(item["id"], fill=random.choice(CONFETTI_COLORS))
            active.append(item)
        else:
            background.delete(item["id"])
    celebration_items[:] = active
    if celebration_items:
        root.after(40, animate_celebration)


def launch_confetti() -> None:
    center_x = root.winfo_width() // 2
    center_y = root.winfo_height() // 2
    for _ in range(80):
        item_id = background.create_text(
            center_x,
            center_y,
            text=random.choice(HEARTS),
            font=("Segoe UI Emoji", random.randint(16, 28)),
            fill=random.choice(CONFETTI_COLORS),
        )
        celebration_items.append(
            {
                "id": item_id,
                "x": center_x,
                "y": center_y,
                "dx": random.uniform(-7.0, 7.0),
                "dy": random.uniform(-7.0, 5.0),
                "life": random.randint(18, 42),
            }
        )
    animate_celebration()


def sparkle_scene() -> None:
    if not accepted:
        return
    x = random.randint(root.winfo_width() // 2 - 260, root.winfo_width() // 2 + 260)
    y = random.randint(root.winfo_height() // 2 - 180, root.winfo_height() // 2 + 180)
    sparkle = background.create_text(
        x,
        y,
        text="✦",
        font=("Georgia", random.randint(14, 22), "bold"),
        fill=random.choice(["#ffffff", "#ffe08a", "#ffb7cb"]),
    )
    root.after(500, lambda current=sparkle: background.delete(current))
    root.after(180, sparkle_scene)


def build_first_page() -> None:
    clear_content()

    eyebrow = tk.Label(
        content_frame,
        text="A little note straight from the heart",
        font=("Georgia", 12, "italic"),
        bg=CARD_BG,
        fg=SECONDARY,
    )
    eyebrow.pack(pady=(4, 8))

    title = tk.Label(
        content_frame,
        text="Will you be my Valentine?",
        font=("Georgia", 30, "bold"),
        bg=CARD_BG,
        fg=TEXT_MAIN,
    )
    title.pack(pady=(0, 12))

    subtitle = tk.Label(
        content_frame,
        text="",
        font=("Segoe UI", 12),
        bg=CARD_BG,
        fg=TEXT_SOFT,
        wraplength=560,
        justify="center",
    )
    subtitle.pack(pady=(0, 24))

    button_row = tk.Frame(content_frame, bg=CARD_BG)
    button_row.pack(pady=(6, 14))

    global yes_button, status_label, no_button
    yes_button = tk.Button(
        button_row,
        text="Yes, with all my heart",
        command=yes_click,
        bg=PRIMARY,
        fg="white",
        activebackground=PRIMARY_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=28,
        pady=14,
        cursor="hand2",
        font=("Segoe UI", yes_font_size, "bold"),
    )
    yes_button.pack(side="left", padx=12)

    status_label = tk.Label(
        content_frame,
        text="The tiny 'No' is feeling extra fluttery.",
        font=("Segoe UI", 11),
        bg=CARD_BG,
        fg=TEXT_SOFT,
    )
    status_label.pack(pady=(0, 12))

    footer = tk.Label(
        content_frame,
        text="Press Esc any time to close",
        font=("Segoe UI", 10),
        bg=CARD_BG,
        fg="#b07a8e",
    )
    footer.pack(pady=(0, 6))

    no_button = tk.Button(
        root,
        text="No",
        command=move_no_button,
        bg="#c58da1",
        fg="white",
        activebackground="#b47a90",
        activeforeground="white",
        relief="flat",
        bd=0,
        cursor="hand2",
        font=("Segoe UI", 12, "bold"),
    )
    no_button.bind("<Enter>", lambda _event: move_no_button())
    place_no_button(initial=True)
    pulse_yes()


def build_second_page() -> None:
    clear_content()
    no_button.place_forget()

    eyebrow = tk.Label(
        content_frame,
        text="Concept 1",
        font=("Georgia", 12, "italic"),
        bg=CARD_BG,
        fg=SECONDARY,
    )
    eyebrow.pack(pady=(8, 8))

    title = tk.Label(
        content_frame,
        text="It's a yes. And it means everything.",
        font=("Georgia", 24, "bold"),
        bg=CARD_BG,
        fg=PRIMARY,
        justify="center",
        wraplength=600,
    )
    title.pack(pady=(0, 14))

    message = tk.Label(
        content_frame,
        text="You didn't just click a button.\nYou created a moment.\n\nSomewhere, a heart just got louder. 💓",
        font=("Segoe UI", 13, "bold"),
        bg=CARD_BG,
        fg=TEXT_MAIN,
        justify="center",
        wraplength=560,
    )
    message.pack(pady=(0, 16))

    note = tk.Label(
        content_frame,
        text="Soft hearts are floating just for you.",
        font=("Segoe UI", 12),
        bg=CARD_BG,
        fg=TEXT_SOFT,
        justify="center",
    )
    note.pack(pady=(0, 16))

    surprise_button = tk.Button(
        content_frame,
        text="See your surprise 🎁",
        command=build_surprise_page,
        bg=PRIMARY,
        fg="white",
        activebackground=PRIMARY_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=24,
        pady=12,
        cursor="hand2",
        font=("Segoe UI", 12, "bold"),
    )
    surprise_button.pack()


def build_surprise_page() -> None:
    clear_content()

    title = tk.Label(
        content_frame,
        text="A hidden little love note",
        font=("Georgia", 30, "bold"),
        bg=CARD_BG,
        fg=PRIMARY,
    )
    title.pack(pady=(24, 18))

    message = tk.Label(
        content_frame,
        text="If this were a real Valentine tucked into your hands,\nit would say:\n\nYou are easy to adore, lovely to think about,\nand the kind of person who can make an ordinary moment feel unforgettable.",
        font=("Segoe UI", 14, "bold"),
        bg=CARD_BG,
        fg=TEXT_MAIN,
        justify="center",
        wraplength=580,
    )
    message.pack(pady=(0, 20))

    note = tk.Label(
        content_frame,
        text="May the rest of your day feel warm, sweet, and kissed by a little magic.",
        font=("Segoe UI", 12),
        bg=CARD_BG,
        fg=TEXT_SOFT,
        justify="center",
        wraplength=560,
    )
    note.pack(pady=(0, 24))

    close_button = tk.Button(
        content_frame,
        text="Close with love",
        command=root.destroy,
        bg=PRIMARY,
        fg="white",
        activebackground=PRIMARY_HOVER,
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=24,
        pady=12,
        cursor="hand2",
        font=("Segoe UI", 12, "bold"),
    )
    close_button.pack()


def yes_click() -> None:
    global accepted
    accepted = True
    build_second_page()
    launch_confetti()
    sparkle_scene()


def on_resize(_event=None) -> None:
    width = max(root.winfo_width(), 1)
    height = max(root.winfo_height(), 1)
    create_gradient(width, height)
    if not background_hearts:
        seed_background_hearts(width, height)
    layout_shell()
    if not accepted:
        place_no_button(initial=False)


root.bind("<Motion>", create_heart_trail)
root.bind("<Configure>", on_resize)

build_first_page()
root.update_idletasks()
create_gradient(root.winfo_width(), root.winfo_height())
seed_background_hearts(root.winfo_width(), root.winfo_height())
layout_shell()
animate_background_hearts()

root.mainloop()

