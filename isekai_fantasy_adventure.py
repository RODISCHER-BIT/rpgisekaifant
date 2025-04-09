import pygame
import random
import time
import sys
import pickle

# Initialize pygame
pygame.init()

# Game constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
MAX_LEVEL = 10
MAX_HP = 100
DUNGEON_SIZE = 5
TOWN_WIDTH, TOWN_HEIGHT = 10, 10
MAX_MAGIC = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (50, 50, 50)

# Fonts
font = pygame.font.SysFont("Arial", 20)

# Setup display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Isekai Fantasy Adventure")

# Sound effects (add sounds to your project directory)
# battle_sound = pygame.mixer.Sound("battle_sound.wav")

# Character class
class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.hp = MAX_HP
        self.attack = 10
        self.magic = 5
        self.level = 1
        self.experience = 0
        self.inventory = []
        self.alive = True
        self.x, self.y = 50, 50  # Position on screen
        self.skills = []  # Special skills
        self.equipment = {
            'weapon': None,
            'armor': None
        }
        self.gold = 50

    def take_damage(self, damage):
        """Reduce HP when taking damage"""
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            print(f"{self.name} has fallen...")

    def heal(self, amount):
        """Heal the character"""
        self.hp = min(MAX_HP, self.hp + amount)
        print(f"{self.name} heals for {amount} HP!")

    def level_up(self):
        """Level up when experience threshold is reached"""
        if self.experience >= self.level * 10:
            self.level += 1
            self.attack += 5
            self.hp = MAX_HP
            self.magic += 2
            self.experience = 0
            print(f"{self.name} has leveled up to level {self.level}!")

    def attack_enemy(self, enemy):
        """Attack an enemy"""
        damage = random.randint(self.attack - 2, self.attack + 2)
        print(f"{self.name} attacks {enemy.name} for {damage} damage!")
        enemy.take_damage(damage)

    def cast_spell(self, enemy):
        """Cast a spell on an enemy"""
        if self.magic >= 3:
            damage = random.randint(10, 20)
            print(f"{self.name} casts a spell on {enemy.name} for {damage} damage!")
            enemy.take_damage(damage)
            self.magic -= 3
        else:
            print(f"{self.name} doesn't have enough magic to cast a spell!")

    def special_attack(self, enemy):
        """Perform a special attack, which has high damage and consumes magic"""
        if self.magic >= 5:
            damage = random.randint(25, 40)
            print(f"{self.name} performs a SPECIAL ATTACK on {enemy.name} for {damage} damage!")
            enemy.take_damage(damage)
            self.magic -= 5
        else:
            print(f"{self.name} doesn't have enough magic to perform a special attack!")

    def equip(self, item):
        """Equip an item"""
        if item.type == 'weapon':
            self.equipment['weapon'] = item
        elif item.type == 'armor':
            self.equipment['armor'] = item
        print(f"{self.name} equips {item.name}.")

    def draw(self, surface):
        """Draw character on the screen"""
        pygame.draw.rect(surface, BLUE, (self.x, self.y, 50, 50))

    def save(self):
        """Save the character's state to a file"""
        with open(f"{self.name}_save.pickle", 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(name):
        """Load the character's state from a file"""
        try:
            with open(f"{name}_save.pickle", 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            print(f"No save file found for {name}. Starting fresh.")
            return None

# Enemy class
class Enemy:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.alive = True

    def take_damage(self, damage):
        """Reduce HP when taking damage"""
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            print(f"{self.name} has been defeated!")

    def attack_character(self, character):
        """Attack the player character"""
        damage = random.randint(self.attack - 2, self.attack + 2)
        print(f"{self.name} attacks {character.name} for {damage} damage!")
        character.take_damage(damage)

    def draw(self, surface, x, y):
        """Draw enemy on the screen"""
        pygame.draw.rect(surface, RED, (x, y, 50, 50))

# Item class
class Item:
    def __init__(self, name, effect, item_type):
        self.name = name
        self.effect = effect
        self.type = item_type

    def use(self, character):
        """Use the item to apply its effect"""
        print(f"{character.name} uses {self.name}.")
        self.effect(character)

# Town class (Simulates the Isekai Town)
class Town:
    def __init__(self):
        self.name = "Isekai Village"
        self.npcs = ["Shopkeeper", "Guild Master", "Mysterious Stranger"]
    
    def enter(self, player):
        print(f"{player.name} enters {self.name}.")
        print("You encounter some NPCs:")
        for npc in self.npcs:
            print(f" - {npc}")
        action = input("Do you wish to (1) Shop, (2) Join Guild, (3) Leave town? ")
        if action == "1":
            self.shop(player)
        elif action == "2":
            self.join_guild(player)
        elif action == "3":
            print("You leave the town and venture into the wild!")

    def shop(self, player):
        """Allows the player to buy items"""
        print(f"{player.name} shops for some healing potions and weapons!")
        item = Item("Healing Potion", lambda p: p.heal(30), 'consumable')
        player.inventory.append(item)
        print(f"Item {item.name} added to inventory.")
        player.gold -= 10

    def join_guild(self, player):
        """Player joins the Guild and gains a skill"""
        print(f"{player.name} joins the Adventurers Guild!")
        player.skills.append("Sword Mastery")
        print("You have unlocked Sword Mastery!")

# Combat function
def combat(player, enemy):
    """Combat between player and enemy"""
    while player.alive and enemy.alive:
        action = input(f"Do you want to (1) Attack, (2) Cast Spell, (3) Special Attack, (4) Defend? ")
        if action == "1":
            player.attack_enemy(enemy)
        elif action == "2":
            player.cast_spell(enemy)
        elif action == "3":
            player.special_attack(enemy)
        elif action == "4":
            print(f"{player.name} defends and reduces incoming damage!")
        else:
            print("Invalid choice. The enemy attacks!")
            enemy.attack_character(player)

        if enemy.alive:
            enemy.attack_character(player)
        else:
            player.experience += 5
            player.level_up()
            break

        if not player.alive:
            break

# Random Events in the world
def random_event():
    """Trigger random events in the game world"""
    events = [
        "You find a hidden treasure chest!",
        "A band of rogue thieves attacks you!",
        "A wizard offers to teach you a powerful spell."
    ]
    return random.choice(events)

# Dungeon class (More intense and challenging environment)
class Dungeon:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.size = random.randint(3, 5)  # Randomize dungeon size

    def explore(self, player):
        """Explore a dungeon, encounter enemies, and get loot"""
        print(f"{player.name} enters a {self.difficulty}-level dungeon!")
        for i in range(self.size):
            print(f"Level {i+1} of the dungeon...")
            enemy = Enemy("Goblin", random.randint(20, 50), random.randint(5, 15))
            combat(player, enemy)
            if not player.alive:
                print(f"{player.name} has fallen in battle!")
                break
        if player.alive:
            print(f"{player.name} has conquered the dungeon!")
            player.gold += 100
            player.experience += 20

# Main game loop
def main():
    """Main game loop"""
    print("Welcome to the Isekai Fantasy Adventure!")
    name = input("Enter your character's name: ")
    class_choice = input("Choose your class (Warrior, Mage, Healer): ").lower()
    
    if class_choice == "warrior":
        player = Character(name, "Warrior")
    elif class_choice == "mage":
        player = Character(name, "Mage")
        player.magic += 10
    elif class_choice == "healer":
        player = Character(name, "Healer")
        player.hp += 30
        player.magic += 5
    else:
        print("Invalid class choice, defaulting to Warrior.")
        player = Character(name, "Warrior")

    # Load or create new character
    action = input("Do you want to (1) Load a saved game or (2) Start a new game? ")
    if action == "1":
        player = Character.load(name)
        if not player:
            print("No save found, starting fresh.")
            player = Character(name, class_choice)
    
    # Initialize screen
    clock = pygame.time.Clock()
    running = True
    town = Town()

    while running and player.alive:
        screen.fill(WHITE)  # Clear screen each frame

        # Draw character and handle movement
        player.draw(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Game interaction
        print(f"Current time: {random_event()}")
        print(f"Your HP: {player.hp} | Level: {player.level} | Experience: {player.experience} | Gold: {player.gold}")
        action = input("Do you want to (1) Explore, (2) Enter Town, (3) Explore Dungeon, (4) Exit Game? ")

        if action == "1":
            print("You venture forth into the unknown...")
            enemy = Enemy("Goblin", 50, 5)
            combat(player, enemy)
        elif action == "2":
            town.enter(player)
        elif action == "3":
            dungeon = Dungeon(difficulty="Medium")
            dungeon.explore(player)
        elif action == "4":
            print("Exiting the game... Goodbye!")
            player.save()  # Save game state
            running = False
        else:
            print("Invalid choice. Try again.")

        # Update display
        pygame.display.update()

        # Frame rate control
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
