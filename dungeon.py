"""The LoreForged Dungeon — data-driven combat prototype v0.2."""
import json
import random
from pathlib import Path
import customtkinter as ctk

DATA_DIR = Path(__file__).resolve().parent / "data"
ctk.set_appearance_mode("Dark")


def read_json(filename):
    with (DATA_DIR / filename).open(encoding="utf-8") as file:
        return json.load(file)


def roll_dice(notation):
    count, sides = map(int, notation.lower().split("d"))
    if not 1 <= count <= 20 or not 2 <= sides <= 100:
        raise ValueError(f"Invalid dice notation: {notation}")
    return sum(random.randint(1, sides) for _ in range(count))


class LoreForgedDungeon(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("The LoreForged Dungeon")
        self.geometry("920x670")
        self.minsize(800, 580)
        self.configure(fg_color="#101d19")
        self.room_index = 0
        self.player_hp = 0
        self.weapon_id = ""
        self.finished = False
        self.new_game()

    def new_game(self):
        # Refresh all game data on restart; no code edits necessary for balancing.
        self.enemies = read_json("enemies.json")
        self.weapons = read_json("weapons.json")
        self.config_data = read_json("dungeon.json")
        self.rooms = self.config_data["rooms"]
        self.player = self.config_data["player"]
        self.player_max_hp = int(self.player["max_health"])
        self.player_hp = self.player_max_hp
        self.weapon_id = self.player["starting_weapon"]
        self.room_index = 0
        self.finished = False
        self.start_encounter()

    def start_encounter(self):
        # Re-read data so updates take effect when entering a new room.
        self.enemies = read_json("enemies.json")
        self.weapons = read_json("weapons.json")
        self.config_data = read_json("dungeon.json")
        self.rooms = self.config_data["rooms"]
        self.room_data = self.rooms[self.room_index]
        self.enemy = self.enemies[self.room_data["enemy"]]
        self.enemy_hp = int(self.enemy["health"])
        self.enemy_max_hp = self.enemy_hp
        self.render_combat()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def label(self, parent, text, size=18, color="#eadbb7"):
        widget = ctk.CTkLabel(
            parent, text=text, font=("Georgia", size), text_color=color,
            wraplength=780, justify="center"
        )
        widget.pack(pady=7)
        return widget

    def button(self, parent, text, command):
        button = ctk.CTkButton(
            parent, text=text, command=command, width=205, height=44,
            fg_color="#87662f", hover_color="#a17c3a"
        )
        button.pack(side="left", padx=8, pady=10)
        return button

    def render_combat(self):
        self.clear()
        self.label(self, "THE LOREFORGED DUNGEON", 30)
        self.label(
            self, f"Room {self.room_index + 1} / {len(self.rooms)} — {self.room_data['name']}", 18
        )
        self.label(self, "Early prototype — art and animations coming later", 12, "#aebba9")

        arena = ctk.CTkFrame(self, fg_color="#20342d")
        arena.pack(fill="x", padx=35, pady=15)
        left = ctk.CTkFrame(arena, fg_color="transparent")
        left.pack(side="left", fill="both", expand=True, pady=18, padx=10)
        right = ctk.CTkFrame(arena, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True, pady=18, padx=10)

        self.label(left, "⚔", 48)
        self.label(left, self.enemy["name"], 21)
        self.enemy_text = self.label(left, "", 16)
        self.enemy_bar = ctk.CTkProgressBar(left, progress_color="#ba514b")
        self.enemy_bar.pack(pady=8)

        self.label(right, "🛡", 48)
        self.label(right, "Adventurer", 21)
        self.player_text = self.label(right, "", 16)
        self.player_bar = ctk.CTkProgressBar(right, progress_color="#62a374")
        self.player_bar.pack(pady=8)
        self.weapon_text = self.label(right, "", 14)

        self.log = self.label(self, f"A {self.enemy['name']} blocks your path!", 17)
        self.actions = ctk.CTkFrame(self, fg_color="transparent")
        self.actions.pack(pady=12)
        self.button(self.actions, "⚔ Attack", self.attack)
        self.update_bars()

    def update_bars(self):
        self.enemy_text.configure(text=f"HP: {self.enemy_hp}/{self.enemy_max_hp}")
        self.player_text.configure(text=f"HP: {self.player_hp}/{self.player_max_hp}")
        self.enemy_bar.set(max(0, self.enemy_hp / max(1, self.enemy_max_hp)))
        self.player_bar.set(max(0, self.player_hp / max(1, self.player_max_hp)))
        weapon = self.weapons[self.weapon_id]
        self.weapon_text.configure(
            text=f"{weapon['name']} · {weapon['damage']} + {weapon['bonus']} damage"
        )

    def attack(self):
        weapon = self.weapons[self.weapon_id]
        roll = random.randint(1, 20)
        attack_total = roll + int(self.player["attack_bonus"])
        if roll == 20 or (roll != 1 and attack_total >= int(self.enemy["defense"])):
            damage = roll_dice(weapon["damage"]) + int(weapon["bonus"])
            self.enemy_hp = max(0, self.enemy_hp - damage)
            message = f"You strike for {damage} damage!"
        else:
            message = "Your attack missed!"

        if self.enemy_hp <= 0:
            self.update_bars()
            if self.room_index == len(self.rooms) - 1:
                self.show_win()
            else:
                self.show_rewards()
            return

        enemy_roll = random.randint(1, 20)
        if enemy_roll == 20 or (
            enemy_roll != 1 and enemy_roll + int(self.enemy["attack_bonus"])
            >= int(self.player["armor_class"])
        ):
            damage = roll_dice(self.enemy["damage"])
            self.player_hp = max(0, self.player_hp - damage)
            message += f"\n{self.enemy['name']} hits you for {damage} damage!"
        else:
            message += f"\n{self.enemy['name']} misses!"

        self.update_bars()
        self.log.configure(text=message)
        if self.player_hp <= 0:
            self.clear_actions()
            self.log.configure(text="You have fallen in battle!")
            self.button(self.actions, "Try Again", self.new_game)

    def clear_actions(self):
        for widget in self.actions.winfo_children():
            widget.destroy()

    def show_rewards(self):
        self.clear_actions()
        heal_amount = int(self.config_data["rewards"]["heal_amount"])
        self.log.configure(
            text=f"Victory over {self.enemy['name']}! Choose ONE reward."
        )
        self.button(self.actions, f"Heal {heal_amount} HP", self.heal)
        self.button(self.actions, "Open Chest", self.open_chest)

    def heal(self):
        heal_amount = int(self.config_data["rewards"]["heal_amount"])
        restored = min(heal_amount, self.player_max_hp - self.player_hp)
        self.player_hp += restored
        self.next_room(f"Recovered {restored} HP!")

    def open_chest(self):
        weapon_id = self.room_data.get("chest_weapon")
        if weapon_id:
            if weapon_id not in self.weapons:
                raise ValueError(f"Unknown chest weapon: {weapon_id}")
            self.weapon_id = weapon_id
            message = f"You equipped {self.weapons[weapon_id]['name']}!"
        else:
            message = "The chest is empty."
        self.next_room(message)

    def next_room(self, message):
        self.room_index += 1
        self.start_encounter()
        self.log.configure(text=message + f"\n{self.enemy['name']} appears!")

    def show_win(self):
        self.clear_actions()
        self.log.configure(text="VICTORY! You defeated the Hydra and escaped the dungeon!")
        self.button(self.actions, "Play Again", self.new_game)


if __name__ == "__main__":
    app = LoreForgedDungeon()
    app.mainloop()
