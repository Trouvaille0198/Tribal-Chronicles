from role import Role
from assistance import *
import random
from functools import reduce
from logger import logger
from name_generator import NameGenerator


class Tribe:
    def __init__(self, game):
        self.name_generator = NameGenerator()  # 一个部落维护一份名字生成器
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

        self.friendship: list = []  # 与其他各族的友好度

    def get_mean_charm(self, gender: None):
        if not gender:
            target_members = [member.real_charm for member in self.members]
        else:
            target_members = [member.real_charm for member in self.members if member.sex == gender]
        return sum(target_members) / self.get_members_num()

    def get_members_num(self):
        return len(self.members)

    def initialize(self):
        self.name = self.name_generator.get_random_last_name()
        self.race = {get_random_race(): 1}
        self.lands.append(random.choice(self.game.world.lands))
        for land in self.lands:
            land.taken = True
        self.food = reduce(lambda x, y: x.food + y.food, self.lands)
        self.mine = reduce(lambda x, y: x.mine + y.mine, self.lands)
        self.members = [Role(self.game) for i in range(random.randint(5, 10))]
        for member in self.members:
            member.create_as_ancestor(self)
        logger.info('由 {} 组成的 {} 部族建立了'.format(self.race, self.name))

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
