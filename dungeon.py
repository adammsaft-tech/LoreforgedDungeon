
import json
import random
from pathlib import Path
import customtkinter as ctk

DATA_FILE = Path(__file__).resolve().parent / "data" / "enemies.json"

ctk.set_appearance_mode("Dark")


class LoreForgedDungeon(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("The LoreForged Dungeon")
        self.geometry("850x620")
        self.configure(fg_color="#101d19")

        self.player_max_hp = 30
        self.player_hp = 30
        self.weapon_bonus = 0
        self.room = 1

        self.start_encounter()

    def start_encounter(self):
        # Reload enemy data for every new encounter.
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            enemies = json.load(file)

        self.enemy = enemies["goblin"]
        self.enemy_hp = self.enemy["health"]
        self.enemy_max_hp = self.enemy_hp

        self.draw_screen()

    def clear(self):
        for widget in self.winfo_children():
            widget.destroy()

    def label(self, parent, text, size=18, color="#eadbb7"):
        widget = ctk.CTkLabel(
            parent, text=text,
            font=("Georgia", size),
            text_color=color
        )
        widget.pack(pady=8)
        return widget

    def draw_screen(self):
        self.clear()

        self.label(self, "THE LOREFORGED DUNGEON", 30)
        self.label(self, f"Room {self.room} - Goblin Warrens", 17)

        arena = ctk.CTkFrame(self, fg_color="#20342d")
        arena.pack(fill="x", padx=35, pady=15)

        enemy_frame = ctk.CTkFrame(arena, fg_color="transparent")
        enemy_frame.pack(side="left", expand=True, padx=20, pady=25)

        player_frame = ctk.CTkFrame(arena, fg_color="transparent")
        player_frame.pack(side="right", expand=True, padx=20, pady=25)

        self.label(enemy_frame, "⚔", 48)
        self.label(enemy_frame, self.enemy["name"], 22)
        self.enemy_text = self.label(enemy_frame, "", 16)
        self.enemy_bar = ctk.CTkProgressBar(
            enemy_frame, progress_color="#ba514b"
        )
        self.enemy_bar.pack(pady=8)

        self.label(player_frame, "🛡", 48)
        self.label(player_frame, "Adventurer", 22)
        self.player_text = self.label(player_frame, "", 16)
        self.player_bar = ctk.CTkProgressBar(
            player_frame, progress_color="#62a374"
        )
        self.player_bar.pack(pady=8)

        self.log = self.label(
            self,
            f"A {self.enemy['name']} blocks your path!",
            17
        )

        self.actions = ctk.CTkFrame(self, fg_color="transparent")
        self.actions.pack(pady=15)

        self.attack_button = ctk.CTkButton(
            self.actions,
            text="⚔ Attack",
            width=170,
            height=45,
            fg_color="#87662f",
            hover_color="#a17c3a",
            command=self.attack
        )
        self.attack_button.pack()

        self.update_bars()

    def update_bars(self):
        self.enemy_text.configure(
            text=f"HP: {self.enemy_hp}/{self.enemy_max_hp}"
        )
        self.player_text.configure(
            text=f"HP: {self.player_hp}/{self.player_max_hp}"
        )

        self.enemy_bar.set(
            max(0, self.enemy_hp / self.enemy_max_hp)
        )
        self.player_bar.set(
            max(0, self.player_hp / self.player_max_hp)
        )

    def attack(self):
        # The player rolls a d20 against enemy defense.
        roll = random.randint(1, 20)
        total = roll + 3

        if roll == 20 or (
            roll != 1 and total >= self.enemy["defense"]
        ):
            damage = random.randint(1, 8) + self.weapon_bonus
            self.enemy_hp = max(0, self.enemy_hp - damage)
            message = f"You hit for {damage} damage!"
        else:
            message = "Your attack missed!"

        if self.enemy_hp <= 0:
            self.update_bars()
            self.show_rewards()
            return

        # Enemy retaliates using its JSON statistics.
        enemy_roll = random.randint(1, 20)
        if enemy_roll + self.enemy["attack_bonus"] >= 12:
            dice = self.enemy["damage"].lower().split("d")
            count, sides = int(dice[0]), int(dice[1])
            damage = sum(
                random.randint(1, sides) for _ in range(count)
            )
            self.player_hp = max(0, self.player_hp - damage)
            message += f"\nEnemy deals {damage} damage!"
        else:
            message += "\nEnemy misses!"

        self.log.configure(text=message)
        self.update_bars()

        if self.player_hp <= 0:
            self.attack_button.configure(state="disabled")
            self.log.configure(text="You have fallen in battle!")
            self.add_button("Try Again", self.restart)

    def add_button(self, title, command):
        ctk.CTkButton(
            self.actions,
            text=title,
            width=190,
            height=42,
            fg_color="#87662f",
            command=command
        ).pack(side="left", padx=8, pady=5)

    def show_rewards(self):
        self.attack_button.destroy()
        self.log.configure(
            text=f"Victory! You defeated the {self.enemy['name']}!"
        )
        self.label(self, "Choose ONE reward:", 20)
        self.add_button("Heal 10 HP", self.heal)
        self.add_button("Open Chest", self.open_chest)

    def heal(self):
        self.player_hp = min(
            self.player_max_hp, self.player_hp + 10
        )
        self.next_room("You recovered health!")

    def open_chest(self):
        self.weapon_bonus += 1
        self.next_room(
            f"Weapon upgraded! Damage bonus: +{self.weapon_bonus}"
        )

    def next_room(self, message):
        self.room += 1
        self.start_encounter()
        self.log.configure(text=message)

    def restart(self):
        self.player_hp = self.player_max_hp
        self.weapon_bonus = 0
        self.room = 1
        self.start_encounter()


if __name__ == "__main__":
    app = LoreForgedDungeon()
    app.mainloop()
