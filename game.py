from world import World
from tribe import Tribe
from race import *
from role import Role
from logger import logger
from checker import PopulationChecker


class Game:
    def __init__(self):
        self.years = 0
        self.world = World(self)
        self.tribes = [Tribe(self) for i in range(10)]

        # checkers
        self.population_checker = PopulationChecker(self)

    def get_all_roles(self):
        return [role for tribe in self.tribes for role in tribe.members]

    def start(self, years: int = 100):
        for i in range(years):
            for tribe in self.tribes:
                tribe.act()
            self.world.land_check()
            self.years += 1
            self.population_checker.round_check()
            logger.info('第{}年，{}个生命'.format(self.years, len(self.get_all_roles())))
        self.population_checker.record_total_data()
        self.population_checker.save_data()


if __name__ == "__main__":
    game = Game()
    game.start(150)
