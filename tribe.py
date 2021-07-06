from role import Role
from utils.utils import *
import random
from logger import logger
from utils.name_generator import NameGenerator


class Tribe:
    def __init__(self, game, init=True):
        self.name_generator = NameGenerator()  # 一个部落维护一份名字生成器
        self.game = game
        self.name: str = ''
        self.race = None
        self.members: list[Role] = []
        self.leader: Role = None
        self.lands: list = []

        self.militancy = 100  # TODO 好战度
        self.stability = 1000  # TODO 稳定度
        if init:
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

    def get_food_num(self):
        result = sum([land.food for land in self.lands]) if self.lands else 0
        return result

    def get_food_consumption(self):
        more_food_tags_num = sum([role for role in self.members if '饕餮' in role.tags])
        less_food_tags_num = sum([role for role in self.members if '厌食' in role.tags])
        consumption = self.get_members_num() * 2 + more_food_tags_num * 2 - less_food_tags_num * 1
        return consumption

    def get_mine_num(self):
        result = sum([land.mine for land in self.lands]) if self.lands else 0
        return result

    def get_mine_consumption(self):
        more_mine_tags_num = sum([role for role in self.members if '贪婪' in role.tags])
        less_mine_tags_num = sum([role for role in self.members if '节俭' in role.tags])
        consumption = self.get_members_num() * 2 + more_mine_tags_num * 2 - less_mine_tags_num * 1
        return consumption

    def initialize(self):
        self.name = self.name_generator.get_random_last_name()
        self.race = get_random_race()
        self.lands.append(random.choice(self.game.world.get_untaken_lands()))
        for land in self.lands:
            land.switch_taken_state()

        self.members = [Role(self.game) for i in range(10)]
        for member in self.members:
            member.create_as_ancestor(self)
        logger.info('由 {} 组成的 {} 部族建立了'.format(self.race, self.name))

    def is_breed_permitted(self):
        if self.get_food_num() < self.get_food_consumption():
            # 当食物量不足时，停止一切繁殖相关动作
            return False
        else:
            return True

    def death_check(self):
        if not self.members:
            self.game.tribes.remove(self)
            for land in self.lands:
                land.switch_taken_state()
            # record
            logger.info('{} 部族后继无人！'.format(self.name))

    def divide_check(self):
        # TODO 稳定度调整
        if self.get_members_num() > 200:
            self.stability = 500
        else:
            self.stability = 1000
        if not is_happened_by_pro(self.stability / 1000):
            self.divide()

    def __str__(self):
        return self.name

    def fight_a_war(self):
        target_tribes = [tribe for tribe in self.game.tribes if tribe != self and tribe.lands]
        if not target_tribes:
            logger.warning('世界上只有一个部落了...')
            return
        target_tribe = random.choice(target_tribes)
        # 各取一半成员
        self_roles = random.sample(self.members, int(self.get_members_num() / 2) + 1)
        target_roles = random.sample(target_tribe.members, int(target_tribe.get_members_num() / 2) + 1)
        # record
        logger.info('{} 向 {} 发起战争！'.format(self.name, target_tribe.name))
        while True:
            self_role = random.choice(self_roles)
            target_role = random.choice(target_roles)
            win_role = self_role.battle(target_role)
            if win_role == self_role:
                target_roles.remove(target_role)
            else:
                self_roles.remove(self_role)
            if not self_roles:
                # 进攻方战败，结束
                logger.info('进攻方 {} 战败！'.format(self.name))
                break
            elif not target_roles:
                # 防御方战败，割地
                target_land = random.choice(target_tribe.lands)
                target_tribe.lands.remove(target_land)
                self.lands.append(target_land)
                logger.info('防守方 {} 战败！将土地 {} 割让'.format(target_tribe.name, target_land.name))
                break
            else:
                continue
        # record
        self.game.population_checker.war_num_yearly += 1

    def find_untaken_land(self):
        target_land = random.choice(self.game.world.get_untaken_lands())
        self.lands.append(target_land)
        target_land.switch_taken_state()
        # record
        logger.info('{} 部族占领了 {}'.format(self.name, target_land.name))

    def divide(self):
        new_tribe = Tribe(self.game, init=False)
        new_tribe.race = self.race
        new_tribe.name = self.name + '_new'
        for _ in range(self.get_members_num() // 2):
            member = random.choice(self.members)
            self.members.remove(member)
            new_tribe.members.append(member)
            member.tribe = new_tribe
        for _ in range(len(self.lands) // 2):
            land = random.choice(self.lands)
            self.lands.remove(land)
            new_tribe.lands.append(land)

        self.game.tribes.append(new_tribe)
        # records
        logger.info('部族{}分裂！'.format(self.name))

    def self_act(self):
        if not self.is_breed_permitted():
            if self.game.world.get_untaken_lands():
                # 若有地未被占领
                if is_happened_by_pro(self.militancy / 1000):
                    # 开战
                    self.fight_a_war()
                else:
                    # 找地
                    self.find_untaken_land()
            else:
                act_by_pro(self.militancy / 1000, self.fight_a_war)
        if self.get_mine_num() < self.get_mine_consumption():
            pass
        self.divide_check()
        self.death_check()

    def act(self):
        self.self_act()  # 部落动作
        for _ in range(4):
            for member in self.members:
                member.act()
