from pokemon import *
import random
from battle_mode import BattleMode

class PokeTeam:
    TEAM_LIMIT = 6

    def __init__(self):
        self.team = (None,) * self.TEAM_LIMIT  # Initialize with None
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
        self.team = tuple(selected + [None] * (self.TEAM_LIMIT - len(selected)))
        self.team_count = len(selected)

    def choose_randomly(self):
        selected = [random.choice(get_all_pokemon_types())() for _ in range(self.TEAM_LIMIT)]
        self.team = tuple(selected)
        self.team_count = len(selected)

    def regenerate_team(self, battle_mode: BattleMode, criterion=None):
        # Regenerate each Pokemon's health, maintain level and evolution
        new_team = []
        for i in range(self.team_count):
            if self.team[i] is not None:
                pokemon = self.team[i]
                pokemon.health = pokemon.max_health  # Assume each Pokemon class has a max_health attribute
                new_team.append(pokemon)
        self.team = tuple(new_team + [None] * (self.TEAM_LIMIT - len(new_team)))
        
    def assemble_team(self, battle_mode: BattleMode):
        if battle_mode == BattleMode.SET:
            # Reverse the tuple for Set Mode
            self.team = self.team[::-1]
        elif battle_mode == BattleMode.ROTATE:
            # Keep as is, rotation will be handled during the battle
            pass
        elif battle_mode == BattleMode.OPTIMISE:
            # Sort based on the criterion initially provided (attribute stored in self.criterion)
            self.team = tuple(sorted(self.team, key=lambda x: getattr(x, self.criterion) if x else 0))

    def special(self, battle_mode: BattleMode):
        mid_point = len(self.team) // 2
        if battle_mode == BattleMode.SET:
            # Reverse the first half of the team
            self.team = self.team[:mid_point][::-1] + self.team[mid_point:]
        elif battle_mode == BattleMode.ROTATE:
            # Reverse the second half of the team
            self.team = self.team[:mid_point] + self.team[mid_point:][::-1]
        elif battle_mode == BattleMode.OPTIMISE:
            # Toggle the sorting order
            self.team = tuple(sorted(self.team, key=lambda x: getattr(x, self.criterion) if x else 0, reverse=True))

    def __getitem__(self, index):
        if index < self.team_count:
            return self.team[index]
        else:
            return None

    def __len__(self):
        return self.team_count

    def __str__(self):
        team_str = "\n".join([str(pokemon) for pokemon in self.team if pokemon is not None])
        return f"Current Team Members:\n{team_str}"

class Trainer:
    def __init__(self, name):
        self.name = name
        self.team = PokeTeam()
        self.pokedex = (False,) * len(PokeType)  # Use a tuple to simulate Pokedex tracking

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
        pokedex_list = list(self.pokedex)
        pokedex_list[index] = True
        self.pokedex = tuple(pokedex_list)

    def get_pokedex_completion(self):
        seen_types = sum(1 for seen in self.pokedex if seen)
        total_types = len(PokeType)
        return round((seen_types / total_types) * 100, 2)

    def __str__(self):
        completion = self.get_pokedex_completion()
        return f"Trainer {self.name} - Pokedex Completion: {completion}%"

if __name__ == '__main__':
    trainer = Trainer('Ash')
    print(trainer)
    trainer.pick_team("random")
    print(trainer)
    print(trainer.get_team())
