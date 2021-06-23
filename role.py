from logger import logger
from race import *
from constants import *
from assistance import *
import random


class Role:
    def __init__(self, game):
        # 基本信息
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
        # 状态
        self.disability: list = []
        self.illness: list = []
        self.wounded_countdown: int = 0
        self.pregnant_obj: Role = None  # 怀孕对象,记录胎儿父亲
        self.pregnant_countdown: int = 0
        self.marry_probability: float = 0
        self.mating_probability: float = 0
        # 属性
        self.wisdom: float = 0
        self.power: float = 0
        self.fertility: float = 0
        self.openness: float = 0
        self.charm: float = 0

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def born(self, **params):
        self.initialize_attributes(**params)
        self.tribe.members.append(self)

    def create_as_ancestor(self, tribe):
        race_dict = tribe.race
        race = sorted(race_dict.items(), key=lambda d: d[1])[0][0]
        params = dict()
        # 基本信息
        params['first_name'] = get_random_name()
        params['last_name'] = get_random_name()
        params['sex'] = random.choice(['male', 'female'])
        params['age'] = 0
        params['race'] = race_dict
        params['lifetime'] = int(normalvariate(race.lifetime, 20))
        params['tribe'] = tribe
        # 特质
        params['height'] = normalvariate(race.height, 12)
        params['weight'] = normalvariate(race.weight, 12)
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
        # 属性
        params['wisdom'] = get_mean_range(get_offset(RaceBase.wisdom, race.wisdom_offset), per_range=0.4)
        params['power'] = get_mean_range(get_offset(RaceBase.power, race.power_offset), per_range=0.4)
        params['fertility'] = get_mean_range(get_offset(RaceBase.fertility, race.fertility_offset), per_range=0.4)
        params['openness'] = get_mean_range(get_offset(RaceBase.openness, race.openness_offset), per_range=0.4)
        params['charm'] = get_mean_range(get_offset(RaceBase.charm, race.charm_offset), per_range=0.4)

        self.initialize_attributes(**params)
        logger.info('{}部族的{}已生成，其属性如下'.format(self.tribe, self.last_name))
        logger.info(params)

    def initialize_attributes(self, first_name, last_name, sex, age, race, lifetime, tribe, height, weight, tags,
                              titles, mother, father, couples, disability, illness, wounded_countdown,
                              pregnant_obj, pregnant_countdown, marry_probability, mating_probability,
                              wisdom, power, fertility, openness, charm):
        """
        初始化各项属性
        """
        # 基本信息
        self.first_name = first_name
        self.last_name = last_name
        self.sex = sex
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
        # 属性
        self.wisdom = wisdom
        self.power = power
        self.fertility = fertility
        self.openness = openness
        self.charm = charm

        self.values_check()

    def give_birth(self):
        baby = Role(self.game)
        params = dict()
        # 基本信息
        params['first_name'] = self.first_name
        params['last_name'] = get_random_name()
        params['sex'] = random.choice(['male', 'female'])
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
        params['marry_probability'] = get_mean_range(self.marry_probability, self.pregnant_obj.marry_probability,
                                                     per_range=0.2)
        params['mating_probability'] = get_mean_range(self.mating_probability, self.pregnant_obj.mating_probability,
                                                      per_range=0.2)
        # 属性
        params['wisdom'] = get_mean_range(self.wisdom + self.pregnant_obj.wisdom, per_range=0.2)
        params['power'] = get_mean_range(self.power + self.pregnant_obj.power, per_range=0.2)
        params['fertility'] = get_mean_range(self.fertility + self.pregnant_obj.fertility, per_range=0.2)
        params['openness'] = get_mean_range(self.openness + self.pregnant_obj.openness, per_range=0.2)
        params['charm'] = get_mean_range(self.charm + self.pregnant_obj.charm, per_range=0.2)

        baby.born(**params)

        return baby

    def get_real_attributes(self) -> dict:
        params = dict()
        # 基本信息
        params['first_name'] = self.first_name
        params['last_name'] = self.last_name
        params['sex'] = self.sex
        params['age'] = self.real_age
        params['race'] = dict(zip(map(lambda x: x.name, self.race.keys()), self.race.values()))
        params['lifetime'] = self.real_lifetime
        params['tribe'] = self.tribe
        # 特质
        params['height'] = self.real_height
        params['weight'] = self.real_weight
        params['tags'] = self.tags
        params['titles'] = self.titles
        # 关系
        params['mother'] = self.mother.get_full_name() if self.mother else 'Born as ancestor'
        params['father'] = self.father.get_full_name() if self.mother else 'Born as ancestor'
        params['couples'] = [role.get_full_name() for role in self.couples] if self.couples else ''
        # 状态
        params['disability'] = self.disability
        params['illness'] = self.illness
        params['wounded_countdown'] = self.wounded_countdown
        params['pregnant_obj'] = self.pregnant_obj
        params['pregnant_countdown'] = self.pregnant_countdown
        params['marry_probability'] = self.real_marry_probability
        params['mating_probability'] = self.real_mating_probability
        # 属性
        params['wisdom'] = self.real_wisdom
        params['power'] = self.real_power
        params['fertility'] = self.real_fertility
        params['openness'] = self.real_openness
        params['charm'] = self.real_charm
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

        self.real_wisdom = offset_by_age(self.wisdom, ABILITY_OFFSET_BY_AGE, self.real_lifetime, self.real_age)
        self.real_power = offset_by_age(self.power, ABILITY_OFFSET_BY_AGE, self.real_lifetime, self.real_age)
        self.real_fertility = offset_by_age(self.fertility, ABILITY_OFFSET_BY_AGE, self.real_lifetime, self.real_age)
        self.real_openness = offset_by_age(self.openness, ABILITY_OFFSET_BY_AGE, self.real_lifetime, self.real_age)
        self.real_charm = offset_by_age(self.charm, ABILITY_OFFSET_BY_AGE, self.real_lifetime, self.real_age)

        self.titles_check()
        self.disability_offset()
        self.illness_offset()
        self.wounded_offset()
        self.pregnant_offset()
        self.tags_offset()

    def titles_check(self):
        pass

    def disability_offset(self):
        pass

    def illness_offset(self):
        pass

    def wounded_offset(self):
        pass

    def pregnant_offset(self):
        pass

    def tags_offset(self):
        pass

    def dead_check(self):
        if self.real_age > self.real_lifetime:
            # logger.debug('{}死亡!'.format(self.get_full_name()))
            self.tribe.members.remove(self)

    def pregnant(self, male_role):
        self.pregnant_countdown = sorted(self.race.items(), key=lambda d: d[1])[0][0].pregnancy
        self.pregnant_obj = male_role

    def childbirth_check(self):
        if self.pregnant_obj and self.pregnant_countdown == 0:
            baby = self.give_birth()
            self.pregnant_obj = None
            # logger.info('{}出生!'.format(baby.get_full_name()))

    def get_married(self):
        """
        TODO 成婚
        """
        roles_around_the_word = list(
            filter(lambda x: x.sex != self.sex and x.real_age >= 16, self.game.get_all_roles()))
        try:
            couple = random.choice(roles_around_the_word)
        except:
            logger.error('random.choice爆了，数组长{}。内容如下'.format(len(roles_around_the_word)))
            logger.info(roles_around_the_word)
            raise ValueError('random.choice爆了，数组长{}。'.format(len(roles_around_the_word)))
        self.couples.append(couple)
        # logger.info('{}与{}喜结连理！时年{}和{}岁'.format(
        #     self.get_full_name(), couple.get_full_name(), self.real_age, couple.real_age))

    def make_love(self):
        """
        TODO 寻欢作乐
        """
        lover = random.choice([role for tribe in self.game.tribes for role in tribe if role.sex != self.sex])

    def love_check(self):
        if (not self.couples or len(self.couples) < 2) and self.real_age >= 16:
            act_by_pro(self.marry_probability, self.get_married)
        if self.couples and not self.pregnant_obj:
            act_by_pro(self.real_fertility / 1000, self.pregnant, random.choice(self.couples))
        self.childbirth_check()

    def act(self):
        """
        回合开始进行操作
        """
        self.wounded_countdown -= 1 if self.wounded_countdown else 0
        self.pregnant_countdown -= 1 if self.pregnant_countdown else 0
        self.age += 1
        self.love_check()
        self.values_check()
        self.dead_check()
        if self.real_age == 20:
            save(self.get_real_attributes(), 'ROLES', str(self.id) + '.txt')
