from assistance import *
import random


class Land():
    max_food: int = 50
    max_mine: int = 50

    def __init__(self):
        self.name = get_random_land_name()
        self.food = Land.max_food
        self.mine = Land.max_mine
        self.taken: bool = False


class World:
    def __init__(self,game):
        self.game=game
        self.lands: list = [Land() for i in range(random.randint(2, 5))]

    def land_check(self):
        for land in self.lands:
            if land.taken:
                if land.food > 0:
                    land.food -= 1
                if land.mine > 0:
                    land.mine -= 1
            else:
                if land.food < Land.max_food:
                    land.food += 1
                if land.mine < Land.max_mine:
                    land.mine += 1
