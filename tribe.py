from role import Role
from assistance import *
import random
from functools import reduce
from logger import logger


class Tribe:
    def __init__(self, game):
        self.game = game
        self.name: str = ''
        self.race: dict = {}
        self.members: list[Role] = []
        self.leader: Role = None
        self.lands: list = []
        self.food: int = 0
        self.mine: int = 0
        self.militancy = 30  # TODO 好战度
        self.stability = 80  # TODO 稳定度
        self.initialize()

    def initialize(self):
        self.name = get_random_name()
        self.race = {get_random_race(): 1}
        self.lands.append(random.choice(self.game.world.lands))
        for land in self.lands:
            land.taken = True
        self.food = reduce(lambda x, y: x.food + y.food, self.lands)
        self.mine = reduce(lambda x, y: x.mine + y.mine, self.lands)
        self.members = [Role(self.game) for i in range(random.randint(5, 10))]
        for member in self.members:
            member.create_as_ancestor(self)
        logger.info('生成一个部族')

    def value_check(self):
        self.food = reduce(lambda x, y: x.food + y.food, self.lands)
        self.mine = reduce(lambda x, y: x.mine + y.mine, self.lands)

    def act(self):
        # TODO 部落动作
        for i in range(4):
            for member in self.members:
                member.act()

    def __str__(self):
        return self.name
