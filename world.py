from utils.utils import *


class Land:
    max_food: float = 50
    max_mine: float = 50

    def __init__(self):
        self.name = get_random_land_name()
        self.type: str = ''
        self.food = Land.max_food
        self.mine = Land.max_mine
        self.taken: bool = False
        self.type_offset()

    def switch_taken_state(self):
        self.taken = not self.taken

    def type_offset(self):
        pass


class World:
    def __init__(self, game, land_num: int):
        self.game = game
        self.lands: list = [Land() for i in range(land_num)]
        # self.lands: list = [Land() for i in range(random.randint(20, 30))]

    def get_all_lands(self):
        return self.lands

    def get_lands_num(self):
        return len(self.lands)

    def get_taken_lands(self):
        return [land for land in self.lands if land.taken]

    def get_untaken_lands(self):
        return [land for land in self.lands if not land.taken]

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
