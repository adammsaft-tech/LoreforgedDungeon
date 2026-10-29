import customtkinter as ctk


def show_character_screen(app):
    app.clear_screen()

    app.grid_rowconfigure(0, weight=0)
    app.grid_rowconfigure(1, weight=1)
    app.grid_rowconfigure(2, weight=0)
    app.grid_columnconfigure(0, weight=1)

    title = ctk.CTkLabel(
        app,
        text="👤 Character Manager",
        font=("Arial", 32, "bold")
    )
    title.grid(row=0, column=0, pady=(25, 10))

    character_frame = ctk.CTkScrollableFrame(
        app,
        label_text="Saved Characters"
    )
    character_frame.grid(
        row=1,
        column=0,
        sticky="nsew",
        padx=30,
        pady=10
    )

    characters = app.load_characters()

    if not characters:
        message = ctk.CTkLabel(
            character_frame,
            text="No characters created yet.",
            font=("Arial", 18)
        )
        message.pack(pady=30)
    else:
        for character in characters:
            name = character.get("name", "Unnamed Character")
            character_class = character.get("class", "Unknown Class")
            level = character.get("level", 1)

            character_button = ctk.CTkButton(
                character_frame,
                text=f"{name} — Level {level} {character_class}",
                width=400,
                height=45,
                command=lambda c=character: app.show_character_details(c)
            )
            character_button.pack(pady=8)

    bottom_frame = ctk.CTkFrame(app)
    bottom_frame.grid(row=2, column=0, pady=(5, 20))

    create_button = ctk.CTkButton(
        bottom_frame,
        text="+ Create Character",
        width=180,
        height=40,
        command=app.show_create_character_screen
    )
    create_button.pack(side="left", padx=10, pady=8)

    back_button = ctk.CTkButton(
        bottom_frame,
        text="← Back",
        width=120,
        height=40,
        command=app.show_home_screen
    )
    back_button.pack(side="left", padx=10, pady=8)


def show_create_character_screen(app):
    app.clear_screen()

    title = ctk.CTkLabel(
        app,
        text="Create Character",
        font=("Arial", 32, "bold")
    )
    title.pack(pady=(30, 20))

    name_label = ctk.CTkLabel(
        app,
        text="Character Name",
        font=("Arial", 18)
    )
    name_label.pack(pady=(10, 5))

    app.character_name_entry = ctk.CTkEntry(
        app,
        width=300,
        height=40,
        placeholder_text="Enter character name"
    )
    app.character_name_entry.pack()

    class_label = ctk.CTkLabel(
        app,
        text="Class",
        font=("Arial", 18)
    )
    class_label.pack(pady=(20, 5))

    app.character_class_entry = ctk.CTkEntry(
        app,
        width=300,
        height=40,
        placeholder_text="Example: Fighter"
    )
    app.character_class_entry.pack()

    level_label = ctk.CTkLabel(
        app,
        text="Level",
        font=("Arial", 18)
    )
    level_label.pack(pady=(20, 5))

    app.character_level_entry = ctk.CTkEntry(
        app,
        width=100,
        height=40,
        placeholder_text="1"
    )
    app.character_level_entry.pack()

    save_button = ctk.CTkButton(
        app,
        text="Save Character",
        width=220,
        height=45,
        command=app.save_character
    )
    save_button.pack(pady=25)

    back_button = ctk.CTkButton(
        app,
        text="← Back",
        width=120,
        command=app.show_character_screen
    )
    back_button.pack(side="bottom", pady=20)