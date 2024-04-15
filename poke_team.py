##########poke_team.py that worked

from pokemon import *
import random
from battle_mode import BattleMode

class PokeTeam:
    TEAM_LIMIT = 6

    def __init__(self):
        self.team = [None] * self.TEAM_LIMIT
        self.team_count = 0

    def choose_manually(self):
        print("Choose up to 6 Pokemon by typing their names:")
        selected = []
        while len(selected) < self.TEAM_LIMIT:
            choice = input(f"Select Pokemon {len(selected) + 1} (or type 'done' to finish): ")
            if choice.lower() == 'done':
                break
            try:
                poke_cls = next(filter(lambda x: x.__name__ == choice, get_all_pokemon_types()))
                selected.append(poke_cls())
            except StopIteration:
                print("Pokemon not found, try again.")
        self.team = selected
        self.team_count = len(selected)

    def choose_randomly(self):
        all_pokemon_classes = get_all_pokemon_types()
        self.team = []

        for _ in range(self.TEAM_LIMIT):
            pokemon_cls = random.choice(all_pokemon_classes)
            self.team.append(pokemon_cls())

        self.team_count = len(self.team)

    def regenerate_team(self, battle_mode: BattleMode, criterion=None):
        for pokemon in self.team:
            if pokemon is not None:
                pokemon.health = pokemon.max_health  # Make sure each Pokemon class has a max_health attribute

    def assemble_team(self, battle_mode: BattleMode):
        if battle_mode == BattleMode.SET:
            self.team.reverse()
        elif battle_mode == BattleMode.OPTIMISE:
            self.team.sort(key=lambda x: getattr(x, criterion, 0))

    def special(self, battle_mode: BattleMode):
        mid_point = len(self.team) // 2
        if battle_mode == BattleMode.SET:
            self.team[:mid_point] = reversed(self.team[:mid_point])
        elif battle_mode == BattleMode.ROTATE:
            self.team[mid_point:] = reversed(self.team[mid_point:])
        elif battle_mode == BattleMode.OPTIMISE:
            self.team.sort(key=lambda x: getattr(x, criterion, 0), reverse=True)

    def __getitem__(self, index):
        return self.team[index] if index < self.team_count else None

    def __len__(self):
        return self.team_count

    def __str__(self):
        return "\n".join(str(pokemon) for pokemon in self.team if pokemon is not None)

class Trainer:
    def __init__(self, name):
        self.name = name
        self.team = PokeTeam()
        self.pokedex = [False] * len(PokeType)

    def pick_team(self, method: str):
        if method.lower() == 'random':
            self.team.choose_randomly()
        elif method.lower() == 'manual':
            self.team.choose_manually()
        else:
            raise ValueError("Invalid team selection method. Choose 'Random' or 'Manual'.")

    def get_team(self):
        return self.team

    def register_pokemon(self, pokemon):
        index = pokemon.get_poketype().value
        self.pokedex[index] = True

    def get_pokedex_completion(self):
        return round(sum(self.pokedex) / len(self.pokedex) * 100, 2)

    def __str__(self):
        completion = self.get_pokedex_completion()
        return f"Trainer {self.name} - Pokedex Completion: {completion}%"

if __name__ == '__main__':
    trainer = Trainer('Ash')
    print(trainer)
    trainer.pick_team("random")
    print(trainer)
    print(trainer.get_team())


