from role import Role
from assistance import *
from logger import logger


class Tribe:
    def __init__(self):
        self.name: str = ''
        self.race: dict = {}
        self.members: list[Role] = []
        self.leader: Role = None
        self.initialize()

    def initialize(self):
        self.name = get_name()
        self.race = {get_random_race(): 1}
        self.members = [Role() for i in range(10)]
        for member in self.members:
            member.create_as_ancestor(self)

    def act(self):
        # TODO 部落动作
        for i in range(4):
            for member in self.members:
                member.act()
