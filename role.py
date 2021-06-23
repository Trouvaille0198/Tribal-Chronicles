from logger import logger
from race import *
from constants import *
from assistance import *
import random


class Role:
    def __init__(self, is_ancestor=False):
        # 基本信息
        self.first_name: str = ''
        self.last_name: str = ''
        self.sex: str = ''
        self.age: float = 0
        self.race: dict = {}
        self.lifetime: int = 0
        self.tribe: Tribe = None
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

    def born(self, **params):
        self.initialize_attributes(**params)

    def create_as_ancestor(self, tribe=None):
        race_dict = tribe.race
        race = sorted(race_dict.items(), key=lambda d: d[1])[0][0]
        params = dict()
        # 基本信息
        params['first_name'] = get_name()
        params['last_name'] = get_name()
        params['sex'] = random.choice(['male', 'female'])
        params['age'] = 0
        params['race'] = race_dict
        params['lifetime'] = get_mean_range(get_offset(RaceBase.lifetime, race.lifetime_offset), per_range=0.3)
        params['tribe'] = tribe
        # 特质
        params['height'] = get_mean_range(get_offset(RaceBase.height, race.height_offset), per_range=0.3)
        params['weight'] = get_mean_range(get_offset(RaceBase.weight, race.weight_offset), per_range=0.3)
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
        self.last_name: last_name
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
        baby = Role()
        params = dict()
        # 基本信息
        params.first_name = self.first_name
        params.last_name = get_name()
        params.sex = random.choice(['male', 'female'])
        params.age = 0
        params.race = get_mixture_race(self.race, self.pregnant_obj.race)
        params.lifetime = get_mean_range(self.lifetime, self.pregnant_obj.lifetime, per_range=0.3)
        params.tribe = self.pregnant_obj.tribe  # TODO 族群认定
        # 特质
        params.height = get_mean_range(self.height, self.pregnant_obj.height, per_range=0.3)
        params.weight = get_mean_range(self.height, self.pregnant_obj.height, per_range=0.3)
        params.tags = []  # TODO 获得先天特性
        params.titles = []  # TODO 头衔继承
        # 关系
        params.mother = self
        params.father = self.pregnant_obj
        params.couples = []
        # 状态
        params.disability = []  # TODO 天生残疾
        params.illness = []  # TODO 天生疾病
        params.wounded_countdown = 0
        params.pregnant_obj = None
        params.pregnant_countdown = 0
        params.marry_probability = get_mean_range(self.marry_probability, self.pregnant_obj.marry_probability,
                                                  per_range=0.4)
        params.mating_probability = get_mean_range(self.mating_probability, self.pregnant_obj.mating_probability,
                                                   per_range=0.4)
        # 属性
        params.wisdom = get_mean_range(self.wisdom + self.pregnant_obj.wisdom, per_range=0.4)
        params.power = get_mean_range(self.power + self.pregnant_obj.power, per_range=0.4)
        params.fertility = get_mean_range(self.fertility + self.pregnant_obj.fertility, per_range=0.4)
        params.openness = get_mean_range(self.openness + self.pregnant_obj.openness, per_range=0.4)
        params.charm = get_mean_range(self.charm + self.pregnant_obj.charm, per_range=0.4)

        baby.born(**params)

    def get_real_attributes(self) -> dict:
        params = dict()
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
            logger.debug('一个个体死亡！')
            self.tribe.members.remove(self)

    def act(self):
        """
        回合开始进行操作
        """
        self.wounded_countdown -= 1 if self.wounded_countdown else 0
        self.pregnant_countdown -= 1 if self.pregnant_countdown else 0
        self.age += 1
        self.values_check()

        self.dead_check()
