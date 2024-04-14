from __future__ import annotations
from poke_team import Trainer, PokeTeam
from typing import Tuple
from battle_mode import BattleMode

class Battle:

    def __init__(self, trainer_1: Trainer, trainer_2: Trainer, battle_mode: BattleMode, criterion = "health") -> None:
        self.trainer_1 = trainer_1
        self.trainer_2 = trainer_2
        self.battle_mode = battle_mode
        self.criterion = criterion

    def _create_teams(self):
        # Prepare teams for battle
        self.trainer_1.team.assemble_team(self.battle_mode)
        self.trainer_2.team.assemble_team(self.battle_mode)

    def commence_battle(self):
        # Start battle based on mode
        if self.battle_mode == BattleMode.SET:
            return self.set_battle()
        elif self.battle_mode == BattleMode.ROTATE:
            return self.rotate_battle()
        elif self.battle_mode == BattleMode.OPTIMISE:
            return self.optimise_battle()

    def set_battle(self):
        # Implement the logic for 'Set' mode battle
        # Details based on initial explanation
        pass

    def rotate_battle(self):
        # Implement the logic for 'Rotate' mode battle
        # Details based on initial explanation
        pass

    def optimise_battle(self):
        # Implement the logic for 'Optimise' mode battle
        # Details based on initial explanation
        pass


if __name__ == '__main__':
    t1 = Trainer('Ash')
    t2 = Trainer('Gary')
    b = Battle(t1, t2, BattleMode.ROTATE)
    b._create_teams()
    winner = b.commence_battle()

    if winner is None:
        print("Its a draw")
    else:
        print(f"The winner is {winner.get_name()}")
