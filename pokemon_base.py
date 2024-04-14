from abc import ABC
from enum import Enum
from data_structures.referential_array import ArrayR

class PokeType(Enum):
    FIRE = 0
    WATER = 1
    GRASS = 2
    BUG = 3
    DRAGON = 4
    ELECTRIC = 5
    FIGHTING = 6
    FLYING = 7
    GHOST = 8
    GROUND = 9
    ICE = 10
    NORMAL = 11
    POISON = 12
    PSYCHIC = 13
    ROCK = 14

class TypeEffectiveness:
    # matrix of effectiveness values from the CSV data provided
    EFFECT_TABLE = (
        (1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 2.0),  # FIRE
        (2.0, 0.5, 0.5, 1.0, 0.5, 1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0),  # WATER
        (0.5, 2.0, 0.5, 0.5, 0.5, 1.0, 1.0, 0.5, 1.0, 2.0, 1.0, 1.0, 0.5, 1.0, 2.0),  # GRASS
        (2.0, 1.0, 2.0, 1.0, 1.0, 1.0, 0.5, 0.5, 0.5, 1.0, 1.0, 1.0, 2.0, 2.0, 2.0),  # BUG
        (1.0, 1.0, 1.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),  # DRAGON
        (1.0, 2.0, 0.5, 1.0, 0.5, 0.5, 1.0, 2.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 1.0),  # ELECTRIC
        (1.0, 1.0, 1.0, 0.5, 1.0, 1.0, 1.0, 0.5, 0.0, 1.0, 2.0, 2.0, 0.5, 0.5, 2.0),  # FIGHTING
        (1.0, 1.0, 2.0, 2.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5),  # FLYING
        (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 0.0, 0.5, 2.0, 1.0),  # GHOST
        (2.0, 1.0, 0.5, 0.5, 1.0, 2.0, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 2.0),  # GROUND
        (1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 0.5, 2.0, 1.0, 2.0, 0.5, 1.0, 1.0, 1.0, 1.0),  # ICE
        (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, 1.0),  # NORMAL
        (1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 1.0, 0.5),  # POISON
        (1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 2.0, 2.0, 0.5, 1.0),  # PSYCHIC
        (0.5, 1.0, 1.0, 2.0, 1.0, 1.0, 0.5, 2.0, 1.0, 0.5, 2.0, 1.0, 1.0, 1.0, 1.0)   # ROCK
    )

    @classmethod
    def get_effectiveness(cls, attack_type: PokeType, defend_type: PokeType) -> float:
        return cls.EFFECT_TABLE[attack_type.value][defend_type.value]

class Pokemon(ABC):
    def __init__(self, name, level, poketype, battle_power, health, defence, speed, experience, evolution_line):
        self.health = health
        self.level = level
        self.poketype = poketype
        self.battle_power = battle_power
        self.evolution_line = evolution_line
        self.name = name
        self.experience = experience
        self.defence = defence
        self.speed = speed

    def get_name(self) -> str:
        return self.name

    def get_health(self) -> int:
        return self.health

    def get_level(self) -> int:
        return self.level

    def get_speed(self) -> int:
        return self.speed

    def get_experience(self) -> int:
        return self.experience

    def get_poketype(self) -> PokeType:
        return self.poketype

    def get_defence(self) -> int:
        return self.defence

    def get_evolution(self):
        return self.evolution_line

    def get_battle_power(self) -> int:
        return self.battle_power

    def attack(self, other_pokemon) -> float:
        effectiveness = TypeEffectiveness.get_effectiveness(self.poketype, other_pokemon.poketype)
        return self.battle_power * effectiveness

    def defend(self, damage: int) -> None:
        effective_damage = damage/2 if damage < self.get_defence() else damage
        self.health = self.health - effective_damage

    def level_up(self):
        self.level += 1
        if len(self.evolution_line) > 1 and self.evolution_line.index(self.name) < len(self.evolution_line) - 1:
            self._evolve()

    def _evolve(self):
        next_index = self.evolution_line.index(self.name) + 1
        self.name = self.evolution_line[next_index]
        self.health = int(self.health * 1.5)
        self.battle_power = int(self.battle_power * 1.5)
        self.speed = int(self.speed * 1.5)
        self.defence = int(self.defence * 1.5)

    def is_alive(self) -> bool:
        return self.get_health() > 0

    def __str__(self):
        return f"{self.name} (Level {self.level}) with {self.get_health()} health and {self.get_experience()} experience"
