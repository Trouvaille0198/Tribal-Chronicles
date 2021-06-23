from world import World
from tribe import Tribe
from race import *
from role import Role
from logger import logger


class Game:
    def __init__(self):
        self.world = World(self)
        self.tribes = [Tribe(self) for i in range(5)]
        self.years = 0

    def get_all_roles(self):
        return [role for tribe in self.tribes for role in tribe.members]

    def start(self, years: int = 100):
        for i in range(years):
            for tribe in self.tribes:
                tribe.act()
            self.world.land_check()
            self.years += 1

            logger.info('第{}年，{}个生命'.format(self.years, len(self.get_all_roles())))


if __name__ == "__main__":
    game = Game()
    game.start(100)
