from poke_team import Trainer, PokeTeam
from enum import Enum
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from typing import Tuple

class BattleTower:
    MIN_LIVES = 1
    MAX_LIVES = 3
    def __init__(self) -> None:
        raise NotImplementedError

    def __init__(self):
        self.player_trainer = None
        self.enemy_trainers = CircularQueue()  # Assuming we have a CircularQueue for holding trainers
        self.enemy_lives = {}  # This should ideally be an ADT but explained here with dict for simplicity
        self.enemies_defeated = 0

    def set_my_trainer(self, trainer: Trainer) -> None:
        self.player_trainer = trainer
        # Randomize player lives within the given range
        self.player_lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)

    def generate_enemy_trainers(self, num_teams: int) -> None:
        for _ in range(num_teams):
            enemy_trainer = Trainer("Enemy_" + str(_))
            enemy_trainer.pick_team("random")  # Assuming this method sets the team in RANDOM mode
            lives = random.randint(self.MIN_LIVES, self.MAX_LIVES)
            self.enemy_trainers.enqueue(enemy_trainer)
            self.enemy_lives[enemy_trainer] = lives  # Storing lives of each trainer

    def battles_remaining(self) -> bool:
        if self.player_lives <= 0 or all(lives <= 0 for lives in self.enemy_lives.values()):
            return False
        return True

    def next_battle(self) -> Tuple[str, Trainer, Trainer, int, int]:
        if not self.battles_remaining():
            return ("No more battles", self.player_trainer, None, self.player_lives, 0)

        current_enemy = self.enemy_trainers.dequeue()
        if self.enemy_lives[current_enemy] > 0:
            # Regenerate teams
            self.player_trainer.team.regenerate_team(BattleMode.ROTATE)
            current_enemy.team.regenerate_team(BattleMode.ROTATE)

            # Conduct battle
            battle = Battle(self.player_trainer, current_enemy, BattleMode.ROTATE)
            winner = battle.commence_battle()

            # Process results
            if winner is None:
                self.player_lives -= 1
                self.enemy_lives[current_enemy] -= 1
                result = "Draw"
            elif winner == self.player_trainer:
                self.enemy_lives[current_enemy] -= 1
                self.enemies_defeated += 1
                result = "Player wins"
            else:
                self.player_lives -= 1
                result = "Enemy wins"

            # Queue the enemy for another round if they still have lives
            if self.enemy_lives[current_enemy] > 0:
                self.enemy_trainers.enqueue(current_enemy)

            return (result, self.player_trainer, current_enemy, self.player_lives, self.enemy_lives[current_enemy])

        return ("Enemy defeated", self.player_trainer, current_enemy, self.player_lives, 0)

    def enemies_defeated(self) -> int:
        return self.enemies_defeated
