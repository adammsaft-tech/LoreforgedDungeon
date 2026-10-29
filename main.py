import customtkinter as ctk
import random
import json
import os

from screens.home_screen import show_home_screen
from screens.dice_screen import show_dice_screen
from screens.character_screen import (
    show_character_screen,
    show_create_character_screen
)


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

MAX_HISTORY = 5

class LoreforgedDeck(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Loreforged Deck")
        self.geometry("800x480")

        self.current_die = 20
        self.roll_animation_count = 0
        self.roll_history = []

        self.show_home_screen()

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def show_home_screen(self):
        show_home_screen(self)

    def show_dice_screen(self):
        show_dice_screen(self)

    def show_character_screen(self):
        show_character_screen(self)

    def show_create_character_screen(self):
        show_create_character_screen(self)

    def save_character(self):
        name = self.character_name_entry.get().strip()
        character_class = self.character_class_entry.get().strip()
        level_text = self.character_level_entry.get().strip()

        if not name or not character_class:
            print("Character name and class are required.")
            return

        try:
            level = int(level_text)
        except ValueError:
            print("Level must be a number.")
            return

        character_data = {
    "name": name,
    "class": character_class,
    "level": level,

    "race": "",
    "background": "",

    "strength": 10,
    "dexterity": 10,
    "constitution": 10,
    "intelligence": 10,
    "wisdom": 10,
    "charisma": 10,

    "hp_current": 10,
    "hp_max": 10,

    "armor_class": 10,
    "initiative": 0,
    "speed": 30,

    "inventory": [],
    "spells": [],
    "notes": ""
}

        characters_folder = os.path.join(
            os.path.dirname(__file__),
            "characters"
        )

        os.makedirs(characters_folder, exist_ok=True)

        safe_filename = "".join(
            character for character in name
            if character.isalnum() or character in (" ", "-", "_")
        ).strip()

        file_path = os.path.join(
            characters_folder,
            f"{safe_filename}.json"
        )

        with open(file_path, "w", encoding="utf-8") as character_file:
            json.dump(character_data, character_file, indent=4)

        print(f"Saved character: {file_path}")
        self.show_character_screen()

    def load_characters(self):
        characters_folder = os.path.join(
            os.path.dirname(__file__),
            "characters"
        )

        os.makedirs(characters_folder, exist_ok=True)

        characters = []

        for filename in os.listdir(characters_folder):
            if filename.endswith(".json"):
                file_path = os.path.join(characters_folder, filename)

                try:
                    with open(file_path, "r", encoding="utf-8") as character_file:
                        character_data = json.load(character_file)

                    character_data["_filename"] = filename
                    characters.append(character_data)

                except (json.JSONDecodeError, OSError) as error:
                    print(f"Could not load {filename}: {error}")

        return characters

    def show_character_details(self, character):
        self.clear_screen()
        self.selected_character = character

        # Character information
        name = character.get("name", "Unnamed Character")
        character_class = character.get("class", "Unknown Class")
        level = character.get("level", 1)
        race = character.get("race", "Unknown Race")

        hp_current = character.get("hp_current", 10)
        hp_max = character.get("hp_max", 10)
        armor_class = character.get("armor_class", 10)
        initiative = character.get("initiative", 0)
        speed = character.get("speed", 30)

        ability_scores = {
            "STR": character.get("strength", 10),
            "DEX": character.get("dexterity", 10),
            "CON": character.get("constitution", 10),
            "INT": character.get("intelligence", 10),
            "WIS": character.get("wisdom", 10),
            "CHA": character.get("charisma", 10)
        }

        # Allow the character sheet to resize properly
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_columnconfigure(0, weight=1)

        # ---------- Header ----------

        header_frame = ctk.CTkFrame(self)
        header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(15, 8)
        )

        name_label = ctk.CTkLabel(
            header_frame,
            text=f"⚔ {name} ⚔",
            font=("Arial", 30, "bold")
        )
        name_label.pack(pady=(10, 2))

        class_label = ctk.CTkLabel(
            header_frame,
            text=f"Level {level} {character_class}",
            font=("Arial", 19)
        )
        class_label.pack()

        race_label = ctk.CTkLabel(
            header_frame,
            text=race,
            font=("Arial", 15)
        )
        race_label.pack(pady=(2, 10))

        # ---------- Scrollable character sheet ----------

        sheet_frame = ctk.CTkScrollableFrame(self)
        sheet_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=20,
            pady=5
        )

        sheet_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        # ---------- Main combat stats ----------

        stat_values = [
            ("❤ HP", f"{hp_current} / {hp_max}"),
            ("🛡 AC", str(armor_class)),
            ("⚡ Initiative", f"{initiative:+d}"),
            ("👣 Speed", f"{speed} ft")
        ]

        for column, (label_text, value_text) in enumerate(stat_values):
            stat_card = ctk.CTkFrame(sheet_frame)
            stat_card.grid(
                row=0,
                column=column,
                sticky="nsew",
                padx=5,
                pady=8
            )

            stat_label = ctk.CTkLabel(
                stat_card,
                text=label_text,
                font=("Arial", 15, "bold")
            )
            stat_label.pack(pady=(10, 3))

            stat_value = ctk.CTkLabel(
                stat_card,
                text=value_text,
                font=("Arial", 22, "bold")
            )
            stat_value.pack(pady=(0, 10))

        # ---------- Ability scores ----------

        ability_title = ctk.CTkLabel(
            sheet_frame,
            text="Ability Scores",
            font=("Arial", 21, "bold")
        )
        ability_title.grid(
            row=1,
            column=0,
            columnspan=4,
            pady=(14, 7)
        )

        for index, (ability, score) in enumerate(ability_scores.items()):
            modifier = (score - 10) // 2
            row = 2 + (index // 3)
            column = index % 3

            ability_card = ctk.CTkFrame(sheet_frame)
            ability_card.grid(
                row=row,
                column=column,
                sticky="nsew",
                padx=6,
                pady=6
            )

            ability_name = ctk.CTkLabel(
                ability_card,
                text=ability,
                font=("Arial", 16, "bold")
            )
            ability_name.pack(pady=(8, 1))

            ability_value = ctk.CTkLabel(
                ability_card,
                text=f"{score}  ({modifier:+d})",
                font=("Arial", 19)
            )
            ability_value.pack(pady=(1, 8))

        # Keep the ability score cards centered
        sheet_frame.grid_columnconfigure(3, minsize=1)

        # ---------- Future feature panels ----------

        section_row = 4

        inventory_frame = ctk.CTkFrame(sheet_frame)
        inventory_frame.grid(
            row=section_row,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=6,
            pady=(15, 6)
        )

        inventory_title = ctk.CTkLabel(
            inventory_frame,
            text="🎒 Inventory",
            font=("Arial", 18, "bold")
        )
        inventory_title.pack(pady=(10, 3))

        inventory_message = ctk.CTkLabel(
            inventory_frame,
            text="Coming soon",
            font=("Arial", 14)
        )
        inventory_message.pack(pady=(0, 10))

        spellbook_frame = ctk.CTkFrame(sheet_frame)
        spellbook_frame.grid(
            row=section_row,
            column=2,
            columnspan=2,
            sticky="nsew",
            padx=6,
            pady=(15, 6)
        )

        spellbook_title = ctk.CTkLabel(
            spellbook_frame,
            text="📜 Spellbook",
            font=("Arial", 18, "bold")
        )
        spellbook_title.pack(pady=(10, 3))

        spellbook_message = ctk.CTkLabel(
            spellbook_frame,
            text="Coming soon",
            font=("Arial", 14)
        )
        spellbook_message.pack(pady=(0, 10))

        notes_frame = ctk.CTkFrame(sheet_frame)
        notes_frame.grid(
            row=section_row + 1,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=6,
            pady=8
        )

        notes_title = ctk.CTkLabel(
            notes_frame,
            text="Notes",
            font=("Arial", 18, "bold")
        )
        notes_title.pack(pady=(10, 3))

        notes_text = character.get("notes", "")
        if not notes_text:
            notes_text = "No notes written yet."

        notes_label = ctk.CTkLabel(
            notes_frame,
            text=notes_text,
            font=("Arial", 14),
            wraplength=650,
            justify="left"
        )
        notes_label.pack(padx=15, pady=(0, 12))

        # ---------- Bottom buttons ----------

        bottom_frame = ctk.CTkFrame(self)
        bottom_frame.grid(
            row=2,
            column=0,
            pady=(5, 15)
        )

        edit_button = ctk.CTkButton(
            bottom_frame,
            text="Edit Character",
            width=170,
            command=self.show_edit_character_screen
        )
        edit_button.pack(side="left", padx=8, pady=8)

        delete_button = ctk.CTkButton(
            bottom_frame,
            text="Delete Character",
            width=170,
            fg_color="darkred",
            hover_color="red",
            command=self.delete_character
        )
        delete_button.pack(side="left", padx=8, pady=8)

        back_button = ctk.CTkButton(
            bottom_frame,
            text="← Back",
            width=120,
            command=self.show_character_screen
        )
        back_button.pack(side="left", padx=8, pady=8)

    def show_edit_character_screen(self):
        self.clear_screen()

        character = self.selected_character

        title = ctk.CTkLabel(
            self,
            text="Edit Character",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(30, 20))

        name_label = ctk.CTkLabel(
            self,
            text="Character Name",
            font=("Arial", 18)
        )
        name_label.pack(pady=(10, 5))

        self.edit_name_entry = ctk.CTkEntry(
            self,
            width=300,
            height=40
        )
        self.edit_name_entry.insert(0, character.get("name", ""))
        self.edit_name_entry.pack()

        class_label = ctk.CTkLabel(
            self,
            text="Class",
            font=("Arial", 18)
        )
        class_label.pack(pady=(20, 5))

        self.edit_class_entry = ctk.CTkEntry(
            self,
            width=300,
            height=40
        )
        self.edit_class_entry.insert(0, character.get("class", ""))
        self.edit_class_entry.pack()

        level_label = ctk.CTkLabel(
            self,
            text="Level",
            font=("Arial", 18)
        )
        level_label.pack(pady=(20, 5))

        self.edit_level_entry = ctk.CTkEntry(
            self,
            width=100,
            height=40
        )
        self.edit_level_entry.insert(0, str(character.get("level", 1)))
        self.edit_level_entry.pack()

        save_button = ctk.CTkButton(
            self,
            text="Save Changes",
            width=220,
            height=45,
            command=self.update_character
        )
        save_button.pack(pady=25)

        back_button = ctk.CTkButton(
            self,
            text="← Cancel",
            width=120,
            command=lambda: self.show_character_details(
                self.selected_character
            )
        )
        back_button.pack(side="bottom", pady=20)

    def update_character(self):
        name = self.edit_name_entry.get().strip()
        character_class = self.edit_class_entry.get().strip()
        level_text = self.edit_level_entry.get().strip()

        if not name or not character_class:
            print("Character name and class are required.")
            return

        try:
            level = int(level_text)
        except ValueError:
            print("Level must be a number.")
            return

        old_filename = self.selected_character.get("_filename")

        if not old_filename:
            print("Could not find the character file.")
            return

        characters_folder = os.path.join(
            os.path.dirname(__file__),
            "characters"
        )

        old_file_path = os.path.join(
            characters_folder,
            old_filename
        )

        safe_filename = "".join(
            character for character in name
            if character.isalnum() or character in (" ", "-", "_")
        ).strip()

        new_filename = f"{safe_filename}.json"
        new_file_path = os.path.join(
            characters_folder,
            new_filename
        )

        updated_character = {
            "name": name,
            "class": character_class,
            "level": level
        }

        with open(new_file_path, "w", encoding="utf-8") as character_file:
            json.dump(updated_character, character_file, indent=4)

        if old_file_path != new_file_path and os.path.exists(old_file_path):
            os.remove(old_file_path)

        updated_character["_filename"] = new_filename
        self.selected_character = updated_character

        self.show_character_details(updated_character)

    def delete_character(self):
        filename = self.selected_character.get("_filename")

        if not filename:
            print("Could not find the character file.")
            return

        file_path = os.path.join(
            os.path.dirname(__file__),
            "characters",
            filename
        )

        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted character: {file_path}")

        self.selected_character = None
        self.show_character_screen()

    def roll_die(self, sides):
        self.current_die = sides
        self.roll_animation_count = 0
        self.animation_speeds = [35, 40, 45, 55, 70, 90, 115, 145, 180, 220]
        self.animate_roll()

    def animate_roll(self):
        temp_roll = random.randint(1, self.current_die)
        self.result_label.configure(text=f"Rolling... {temp_roll}")

        if self.roll_animation_count < len(self.animation_speeds):
            delay = self.animation_speeds[self.roll_animation_count]
            self.roll_animation_count += 1
            self.after(delay, self.animate_roll)
        else:
            self.finish_roll()

    def finish_roll(self):
        try:
            modifier = int(self.modifier_entry.get())
        except ValueError:
            modifier = 0

        roll = random.randint(1, self.current_die)
        total = roll + modifier

        if self.current_die == 20 and roll == 20:
            result_text = f"✨ NATURAL 20! ✨\nD20: {roll} + {modifier} = {total}"
        elif self.current_die == 20 and roll == 1:
            result_text = f"💀 NATURAL 1! 💀\nD20: {roll} + {modifier} = {total}"
        else:
            result_text = f"D{self.current_die}: {roll} + {modifier} = {total}"

        self.result_label.configure(text=result_text)
        self.add_to_history(
            f"D{self.current_die}: {roll} + {modifier} = {total}"
        )

    def add_to_history(self, roll_text):
        self.roll_history.insert(0, roll_text)

        if len(self.roll_history) > MAX_HISTORY:
            self.roll_history.pop()

        self.history_label.configure(
            text="\n".join(self.roll_history)
        )

    def clear_history(self):
        self.roll_history.clear()
        self.history_label.configure(text="")


app = LoreforgedDeck()
app.mainloop()