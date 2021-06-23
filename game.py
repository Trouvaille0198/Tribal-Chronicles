from world import World
from tribe import Tribe
from race import *
from role import Role
from logger import logger


class Game:
    def __init__(self):
        self.world = World()
        self.tribes = [Tribe() for i in range(5)]
        self.years = 0

    def start(self, years: int = 100):
        for i in range(years):
            for tribe in self.tribes:
                tribe.act()
            self.years += 1
            logger.info('第{}年'.format(self.years))


if __name__ == "__main__":
    game = Game()
    game.start(5000)
