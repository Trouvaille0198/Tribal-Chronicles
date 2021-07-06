import time
from world import World
from tribe import Tribe
from logger import logger
from utils.checker import PopulationChecker


class Game:
    def __init__(self):
        self.years = 0
        self.world = World(self, land_num=120)
        self.tribes = [Tribe(self) for i in range(20)]
        # self.tribes = [Tribe(self) for i in range(random.randint(8, 12))]

        # checkers
        self.population_checker = PopulationChecker(self)

    def get_all_roles(self):
        return [role for tribe in self.tribes for role in tribe.members]

    def get_roles_num(self):
        return len(self.get_all_roles())

    def get_tribes_num(self):
        return len(self.tribes)

    def start(self, years: int = 100):
        for i in range(years):
            self.years += 1
            logger.info('第{}年，{}个生命'.format(self.years, len(self.get_all_roles())))
            print('第{}年，{}个生命'.format(self.years, len(self.get_all_roles())))
            for tribe in self.tribes:
                tribe.act()
            # self.world.land_check()

            # record
            self.population_checker.round_check()

        # record
        self.population_checker.record_total_data()
        self.population_checker.save_data()


if __name__ == "__main__":
    start = time.time()
    game = Game()
    game.start(500)
    end = time.time()
    print('总共用时 {}s'.format(end - start))
