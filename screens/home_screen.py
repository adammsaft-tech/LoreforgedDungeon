import customtkinter as ctk


def show_home_screen(app):
    app.clear_screen()

    title = ctk.CTkLabel(
        app,
        text="⚔ Loreforged Deck ⚔",
        font=("Arial", 36, "bold")
    )
    title.pack(pady=(50, 10))

    subtitle = ctk.CTkLabel(
        app,
        text="Adventurer's Companion",
        font=("Arial", 18)
    )
    subtitle.pack(pady=(0, 40))

    dice_button = ctk.CTkButton(
        app,
        text="🎲 Dice Roller",
        width=250,
        height=45,
        font=("Arial", 18),
        command=app.show_dice_screen
    )
    dice_button.pack(pady=10)

    character_button = ctk.CTkButton(
        app,
        text="👤 Characters",
        width=250,
        height=45,
        font=("Arial", 18),
        command=app.show_character_screen
    )
    character_button.pack(pady=10)

    settings_button = ctk.CTkButton(
        app,
        text="⚙ Settings",
        width=250,
        height=45,
        font=("Arial", 18)
    )
    settings_button.pack(pady=10)

    version = ctk.CTkLabel(
        app,
        text="Version 0.2",
        font=("Arial", 12)
    )
    version.pack(side="bottom", pady=10)
    