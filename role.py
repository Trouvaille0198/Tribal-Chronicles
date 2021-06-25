from logger import logger
from race import *
from constants import *
from assistance import *
import random


class Role:
    def __init__(self, game):
        # 基本信息
        self.birth_year: int = 0
        self.game = game
        self.id = random.randint(10000, 99999)
        self.first_name: str = ''
        self.last_name: str = ''
        self.sex: str = ''
        self.age: float = 0
        self.race: dict = {}
        self.lifetime: int = 0
        self.tribe = None
        # 特质
        self.height: float = 0
        self.weight: float = 0
        self.tags: list = []
        self.titles: list = []
        # 关系
        self.mother: Role = None
        self.father: Role = None
        self.couples: list[Role] = []
        self.baby_unborn: list = []
        # 状态
        self.disability: list = []
        self.illness: list = []
        self.wounded_countdown: int = 0
        self.pregnant_obj: Role = None  # 怀孕对象,记录胎儿父亲
        self.pregnant_countdown: int = 0
        self.marry_probability: float = 0  # 成婚意愿 每回合做出结婚动作的概率
        self.mating_probability: float = 0  # 交配意愿 每回合做出交配动作的概率
        self.fertility_probability: float = 0  # 成产率
        # 能力属性
        self.wisdom: float = 0  # 智慧
        self.power: float = 0  # 力量
        self.openness: float = 0  # 开放程度
        self.charm: float = 0  # 魅力
        # 修正属性
        self.real_age: int = 0
        self.real_lifetime: int = 0
        self.real_height: float = 0
        self.real_weight: float = 0
        self.real_marry_probability: float = 0
        self.real_mating_probability: float = 0
        self.real_fertility_probability: float = 0

        self.real_wisdom: float() = 0
        self.real_power: float() = 0
        self.real_openness: float() = 0
        self.real_charm: float() = 0
        # 其他莫名其妙的统计信息
        self.make_love_num: int = 0  # 干人次数(?
        self.child_num: int = 0
        self.win_num: int = 0

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_main_race(self):
        return sorted(self.race.items(), key=lambda d: -d[1])[0][0]

    def is_marry_permitted(self):
        if self.real_age > 14:
            if self.sex == 'female' and not self.couples and not self.pregnant_obj:
                return True
            if self.sex == 'male' and (not self.couples or len(self.couples) < 2):
                return True
        return False

    def born(self, **params):
        self.initialize_attributes(**params)
        self.tribe.members.append(self)
        # record

    def create_as_ancestor(self, tribe):
        race = tribe.race
        params = dict()
        # 基本信息
        params['sex'] = random.choice(['male', 'female'])
        params['first_name'] = tribe.name_generator.get_random_first_name(params['sex'])
        params['last_name'] = tribe.name
        params['birth_year'] = self.game.years
        params['age'] = 0
        params['race'] = {race: 1}
        params['lifetime'] = int(get_mean_range(race.lifetime, per_range=0.2))
        params['tribe'] = tribe
        # 特质
        params['height'] = get_mean_range(race.height, per_range=0.2)
        params['weight'] = get_mean_range(race.weight, per_range=0.2)
        params['tags'] = []  # TODO 获得先天特性
        params['titles'] = []  # TODO 头衔继承
        # 关系
        params['mother'] = None
        params['father'] = None
        params['couples'] = []
        # 状态
        params['disability'] = []  # TODO 天生残疾
        params['illness'] = []  # TODO 天生疾病
        params['wounded_countdown'] = 0
        params['pregnant_obj'] = None
        params['pregnant_countdown'] = 0
        params['marry_probability'] = get_mean_range(get_offset(RaceBase.marry_probability, race.marry_offset),
                                                     per_range=0.3)
        params['mating_probability'] = get_mean_range(get_offset(RaceBase.mating_probability, race.mating_offset),
                                                      per_range=0.3)
        params['fertility_probability'] = get_mean_range(
            get_offset(RaceBase.fertility_probability, race.fertility_offset),
            per_range=0.3)
        # 属性
        params['wisdom'] = get_mean_range(get_offset(RaceBase.wisdom, race.wisdom_offset), per_range=0.4)
        params['power'] = get_mean_range(get_offset(RaceBase.power, race.power_offset), per_range=0.4)
        params['openness'] = get_mean_range(get_offset(RaceBase.openness, race.openness_offset), per_range=0.4)
        params['charm'] = get_mean_range(get_offset(RaceBase.charm, race.charm_offset), per_range=0.4)

        self.initialize_attributes(**params)
        # logger.info('{}部族的{}已生成，其属性如下'.format(self.tribe, self.last_name))
        # logger.info(params)

    def initialize_attributes(self, first_name, last_name, sex, birth_year, age, race, lifetime, tribe, height, weight,
                              tags,
                              titles, mother, father, couples, disability, illness, wounded_countdown,
                              pregnant_obj, pregnant_countdown, marry_probability, mating_probability,
                              fertility_probability, wisdom, power, openness, charm):
        """
        初始化各项属性
        """
        # 基本信息
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
        self.birth_year = birth_year
        self.age = age
        self.race = race
        self.lifetime = lifetime
        self.tribe = tribe
        # 特质
        self.height = height
        self.weight = weight
        self.tags = tags
        self.titles = titles
        # 关系
        self.mother = mother
        self.father = father
        self.couples = couples
        # 状态
        self.disability = disability
        self.illness = illness
        self.wounded_countdown = wounded_countdown
        self.pregnant_obj = pregnant_obj
        self.pregnant_countdown = pregnant_countdown
        self.marry_probability = marry_probability
        self.mating_probability = mating_probability
        self.fertility_probability = fertility_probability
        # 属性
        self.wisdom = wisdom
        self.power = power
        self.openness = openness
        self.charm = charm

        self.values_check()

    def give_birth(self):
        baby = self.baby_unborn[0]
        params = dict()
        # 基本信息
        params['sex'] = random.choice(['male', 'female'])
        params['first_name'] = self.tribe.name_generator.get_random_first_name(params['sex'])
        params['last_name'] = self.pregnant_obj.last_name
        params['birth_year'] = self.game.years
        params['age'] = 0
        params['race'] = get_mixture_race(self.race, self.pregnant_obj.race)
        params['lifetime'] = get_mean_range(self.lifetime, self.pregnant_obj.lifetime, per_range=0.3)
        params['tribe'] = self.pregnant_obj.tribe  # TODO 族群认定
        # 特质
        params['height'] = get_mean_range(self.height, self.pregnant_obj.height, per_range=0.2)
        params['weight'] = get_mean_range(self.weight, self.pregnant_obj.weight, per_range=0.2)
        params['tags'] = []  # TODO 获得先天特性
        params['titles'] = []  # TODO 头衔继承
        # 关系
        params['mother'] = self
        params['father'] = self.pregnant_obj
        params['couples'] = []
        # 状态
        params['disability'] = []  # TODO 天生残疾
        params['illness'] = []  # TODO 天生疾病
        params['wounded_countdown'] = 0
        params['pregnant_obj'] = None
        params['pregnant_countdown'] = 0
        params['marry_probability'] = get_mean_range(self.marry_probability,
                                                     self.pregnant_obj.marry_probability, per_range=0.2)
        params['mating_probability'] = get_mean_range(self.mating_probability,
                                                      self.pregnant_obj.mating_probability, per_range=0.2)
        params['fertility_probability'] = get_mean_range(self.fertility_probability,
                                                         self.pregnant_obj.fertility_probability, per_range=0.2)
        # 属性
        params['wisdom'] = get_mean_range(self.wisdom, self.pregnant_obj.wisdom, per_range=0.2)
        params['power'] = get_mean_range(self.power, self.pregnant_obj.power, per_range=0.2)
        params['openness'] = get_mean_range(self.openness, self.pregnant_obj.openness, per_range=0.2)
        params['charm'] = get_mean_range(self.charm, self.pregnant_obj.charm, per_range=0.2)

        baby.born(**params)

        return baby

    def get_all_attributes(self) -> dict:
        params = dict()
        # 基本信息
        params['first_name'] = self.first_name
        params['last_name'] = self.last_name
        params['sex'] = self.sex
        params['birth_year'] = self.birth_year
        params['age'] = self.real_age
        params['lifetime'] = self.real_lifetime
        params['race'] = dict(sorted(dict(zip(map(lambda x: x.name, self.race.keys()), self.race.values())).items(),
                                     key=lambda y: -y[1]))
        params['tribe'] = self.tribe
        # 特质
        params['base height'] = self.height
        params['base weight'] = self.weight
        params['real_height'] = self.real_height
        params['real_weight'] = self.real_weight
        params['tags'] = self.tags
        params['titles'] = self.titles
        # 关系
        params['mother'] = self.mother.get_full_name() if self.mother else 'Born as ancestor'
        params['father'] = self.father.get_full_name() if self.mother else 'Born as ancestor'
        params['couples'] = [role.get_full_name() for role in self.couples] if self.couples else ['']
        # 统计属性
        params['make_love_num'] = self.make_love_num
        params['child num'] = self.child_num
        params['win_num'] = self.win_num
        # 状态
        params['disability'] = self.disability
        params['illness'] = self.illness
        # params['wounded_countdown'] = self.wounded_countdown
        # params['pregnant_obj'] = self.pregnant_obj
        # params['pregnant_countdown'] = self.pregnant_countdown
        params['base_marry_probability'] = self.marry_probability
        params['base_mating_probability'] = self.mating_probability
        params['base_fertility_probability'] = self.fertility_probability
        # 属性
        params['base wisdom'] = self.wisdom
        params['base power'] = self.power
        params['base openness'] = self.openness
        params['base charm'] = self.charm

        # params['real_marry_probability'] = self.real_marry_probability
        # params['real_mating_probability'] = self.real_mating_probability
        # params['real_fertility_probability'] = self.real_fertility_probability
        # params['real_wisdom'] = self.real_wisdom
        # params['real_power'] = self.real_power
        # params['real_openness'] = self.real_openness
        # params['real_charm'] = self.real_charm

        return params

    def values_check(self):
        """
        修正数值
        """
        self.real_age = int(self.age / 4)
        self.real_lifetime = self.lifetime

        self.real_height = offset_by_age(self.height, HEIGHT_OFFSET_BY_AGE, self.real_lifetime, self.real_age)
        self.real_weight = offset_by_age(self.weight, WEIGHT_OFFSET_BY_AGE, self.real_lifetime, self.real_age)

        self.real_mating_probability = offset_by_age(self.mating_probability, MATING_OFFSET_BY_AGE, self.real_lifetime,
                                                     self.real_age)
        self.real_marry_probability = offset_by_age(self.marry_probability, MARRY_OFFSET_BY_AGE, self.real_lifetime,
                                                    self.real_age)
        self.real_fertility_probability = offset_by_age(self.fertility_probability, FERTILITY_OFFSET_BY_AGE,
                                                        self.real_lifetime, self.real_age)

        self.real_wisdom = offset_by_age(self.wisdom, WISDOM_OFFSET_BY_AGE, self.real_lifetime, self.real_age)
        self.real_power = offset_by_age(self.power, ABILITY_OFFSET_BY_AGE, self.real_lifetime, self.real_age)
        self.real_openness = offset_by_age(self.openness, ABILITY_OFFSET_BY_AGE, self.real_lifetime, self.real_age)
        self.real_charm = offset_by_age(self.charm, ABILITY_OFFSET_BY_AGE, self.real_lifetime, self.real_age)

        self.married_offset()
        self.titles_offset()
        self.disability_offset()
        self.illness_offset()
        self.wounded_offset()
        self.pregnant_offset()
        self.tags_offset()

    def married_offset(self):
        if self.couples:
            self.real_fertility_probability = get_offset(self.real_fertility_probability, 0.1)
            self.real_mating_probability = get_offset(self.real_mating_probability, 0.2)

    def titles_offset(self):
        pass

    def disability_offset(self):
        pass

    def illness_offset(self):
        pass

    def wounded_offset(self):
        if self.wounded_countdown:
            self.real_power = get_offset(self.real_power, -0.3)

    def pregnant_offset(self):
        pass

    def tags_offset(self):
        pass

    def dead_check(self):
        if self.real_age > self.real_lifetime:
            self.tags.append('老死')
            self.die()

    def die(self):
        self.game.population_checker.death_num_yearly += 1
        # logger.debug('{}死亡!'.format(self.get_full_name()))
        save(self.get_all_attributes(), 'RECORDS\\ROLES', self.get_full_name() + '.txt')
        self.tribe.members.remove(self)

    def pregnant(self, male_role, is_illegitimate=False):
        self.pregnant_countdown = self.get_main_race().pregnancy
        self.pregnant_obj = male_role
        baby = Role(self.game)
        if is_illegitimate:
            baby.titles.append('私生子')
        self.baby_unborn.append(baby)
        # record
        self.game.population_checker.pregnant_num_yearly += 1
        # logger.info('{}怀孕了，时年{}岁'.format(self.get_full_name(), self.real_age))

    def childbirth_check(self):
        if self.pregnant_obj and self.pregnant_countdown == 0:
            if is_happened_by_pro(self.real_fertility_probability / 1000):
                baby = self.give_birth()
                self.child_num += 1
                self.pregnant_obj.child_num += 1
                # record
                self.game.population_checker.born_num_yearly += 1
                # logger.info('{}生子，时年{}岁'.format(self.get_full_name(), self.real_age))
                # logger.info('{}出生!'.format(baby.get_full_name()))
            else:
                # record
                self.game.population_checker.abortion_num_yearly += 1
                # logger.info('{}流产，时年{}岁'.format(self.get_full_name(), self.real_age))
            self.pregnant_obj = None
            self.baby_unborn.pop(0)

    def get_married(self):
        """
        TODO 成婚
        """
        # 异种判定
        if is_happened_by_pro(self.real_openness / 1000):
            roles = list(
                filter(lambda
                           x: x.sex != self.sex and x.is_marry_permitted() and x.get_main_race() != self.get_main_race(),
                       self.game.get_all_roles()))
        else:
            if is_happened_by_pro(0.1):
                # 异族
                roles = list(
                    filter(lambda
                               x: x.sex != self.sex
                                  and x.is_marry_permitted()
                                  and x.get_main_race() == self.get_main_race()
                                  and self.tribe != x.tribe,
                           self.game.get_all_roles()))
            else:
                # 同族
                roles = list(
                    filter(lambda
                               x: x.sex != self.sex
                                  and x.is_marry_permitted()
                                  and x.get_main_race() == self.get_main_race()
                                  and self.tribe == x.tribe,
                           self.game.get_all_roles()))
        if not roles:
            return
        couple = random.choice(roles)
        charm_pro = self.real_charm / (self.real_charm + couple.tribe.get_mean_charm(self.sex))
        if is_happened_by_pro(charm_pro):
            # 求偶成功辣
            self.couples.append(couple)
            couple.couples.append(self)
            # record
            if self.get_main_race() != couple.get_main_race():
                self.game.population_checker.marry_diff_race_yearly += 1
            elif self.tribe != couple.tribe:
                self.game.population_checker.marry_diff_tribe_yearly += 1
            else:
                pass
            self.game.population_checker.marry_num_yearly += 1
            # logger.info('{}与{}喜结连理！时年{}和{}岁'.format(
            # self.get_full_name(), couple.get_full_name(), self.real_age, couple.real_age))

    def make_love(self):
        """
        TODO 寻欢作乐
        """
        couples_no_preg = [couple for couple in self.couples if not couple.pregnant_obj]
        if couples_no_preg:
            # 若存在未怀孕的伴侣
            lover = random.choice(couples_no_preg)
            if self.sex == 'female':
                act_by_pro(lover.real_fertility_probability / 1000, self.pregnant, lover, True)
            else:
                act_by_pro(self.real_fertility_probability / 1000, lover.pregnant, self, True)
            # record
            lover.make_love_num += 1
            self.make_love_num += 1
            self.game.population_checker.make_love_num_yearly += 1
        else:
            lovers = list(
                filter(lambda x: x.sex != self.sex and not x.pregnant_obj, self.game.get_all_roles()))
            if not lovers:
                # logger.warning('竟然没有未怀孕的人儿了？！')
                return
            lover = random.choice(lovers)
            charm_pro = self.real_charm / (self.real_charm + lover.real_charm)
            if is_happened_by_pro(charm_pro):
                if self.sex == 'female':
                    act_by_pro(lover.real_fertility_probability / 1000, self.pregnant, lover, True)
                else:
                    act_by_pro(self.real_fertility_probability / 1000, lover.pregnant, self, True)
                # record
                self.game.population_checker.make_love_num_yearly += 1
                lover.make_love_num += 1
                self.make_love_num += 1

    def love_check(self):
        # 成婚判定
        if self.is_marry_permitted():
            act_by_pro(self.real_marry_probability / 1000, self.get_married)
        # 交媾判定
        if not self.pregnant_obj:
            act_by_pro(self.real_mating_probability / 1000, self.make_love)
        self.childbirth_check()

    def battle(self, target_role):
        """
        战斗判定
        :param target_role: 对手
        :return: 胜者
        """
        pro = self.real_power / (self.real_power + target_role.real_power)
        if is_happened_by_pro(pro):
            win_role = self
            self.win_num += 1
            target_role.hurt_check()
        else:
            win_role = target_role
            target_role.win_num += 1
            self.hurt_check()
        return win_role

    def hurt_check(self):
        if not is_happened_by_pro(self.real_wisdom / 1000):
            if not is_happened_by_pro(self.real_wisdom / 4000):
                self.tags.append('战死')
                self.die()
                # record
                # logger.info('{} 战死！'.format(self.get_full_name()))
                self.game.population_checker.die_by_war_num_yearly += 1
            else:
                self.get_wounded()

    def get_wounded(self):
        self.wounded_countdown += random.randint(5, 20)
        # TODO 致残判定
        if not is_happened_by_pro(self.real_wisdom / 2000):
            self.tags.append('残疾')

    def act(self):
        """
        回合开始进行操作
        """
        self.wounded_countdown -= 1 if self.wounded_countdown else 0
        self.pregnant_countdown -= 1 if self.pregnant_countdown else 0
        self.age += 1
        if self.tribe.is_breed_permitted():
            self.love_check()
        self.values_check()
        self.dead_check()
