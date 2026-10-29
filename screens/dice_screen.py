import customtkinter as ctk


def show_dice_screen(app):
    app.clear_screen()

    # Make the window use rows so the bottom buttons stay visible
    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=0)
    app.grid_rowconfigure(2, weight=0)
    app.grid_rowconfigure(3, weight=1)
    app.grid_rowconfigure(4, weight=0)
    app.grid_columnconfigure(0, weight=1)

    # Title
    title = ctk.CTkLabel(
        app,
        text="🎲 Dice Roller",
        font=("Arial", 34, "bold")
    )
    title.grid(row=0, column=0, pady=(15, 8))

    # Dice buttons
    dice_frame = ctk.CTkFrame(app)
    dice_frame.grid(row=1, column=0, padx=20, pady=5)

    dice = [4, 6, 8, 10, 12, 20, 100]

    for die in dice:
        button = ctk.CTkButton(
            dice_frame,
            text=f"D{die}",
            width=90,
            height=45,
            font=("Arial", 16),
            command=lambda d=die: app.roll_die(d)
        )
        button.pack(side="left", padx=5, pady=10)

    # Modifier and result section
    result_frame = ctk.CTkFrame(app)
    result_frame.grid(row=2, column=0, padx=20, pady=5)

    modifier_label = ctk.CTkLabel(
        result_frame,
        text="Modifier",
        font=("Arial", 18)
    )
    modifier_label.pack(pady=(8, 4))

    app.modifier_entry = ctk.CTkEntry(
        result_frame,
        width=100,
        font=("Arial", 18),
        justify="center"
    )
    app.modifier_entry.insert(0, "0")
    app.modifier_entry.pack()

    app.result_label = ctk.CTkLabel(
        result_frame,
        text="Choose a die!",
        font=("Arial", 28, "bold")
    )
    app.result_label.pack(pady=10)

    # Scrollable roll history
    history_frame = ctk.CTkScrollableFrame(
        app,
        label_text="Roll History",
        height=110
    )
    history_frame.grid(
        row=3,
        column=0,
        sticky="nsew",
        padx=20,
        pady=5
    )

    app.history_label = ctk.CTkLabel(
        history_frame,
        text="",
        font=("Arial", 16),
        justify="left",
        anchor="w"
    )
    app.history_label.pack(fill="x", padx=10, pady=5)

    # Bottom navigation
    bottom_frame = ctk.CTkFrame(app)
    bottom_frame.grid(row=4, column=0, padx=20, pady=(5, 15))

    clear_button = ctk.CTkButton(
        bottom_frame,
        text="Clear History",
        width=140,
        command=app.clear_history
    )
    clear_button.pack(side="left", padx=10, pady=8)

    back_button = ctk.CTkButton(
        bottom_frame,
        text="← Back",
        width=120,
        command=app.show_home_screen
    )
    back_button.pack(side="left", padx=10, pady=8)