class RaceBase:
    lifetime: int = 100
    pregnancy: int = 4
    sex: bool = True
    militancy: float = 0
    mating_probability: float = 100
    marry_probability: float = 15
    fertility_probability: float = 500
    # 能力作为概率使用时，以千分号为单位
    wisdom: float = 500  # 绝对概率
    power: float = 500  # 相对概率
    openness: float = 50  # 绝对概率
    charm: float = 500  # 相对概率

    height: float = 170
    weight: float = 65


class Humankind(RaceBase):
    name: str = "Humankind"
    # 基础属性改动
    lifetime = 60
    pregnancy = 6
    sex = True
    militancy_offset = 0
    mating_offset = 0
    marry_offset = 0
    fertility_offset = 0
    # 属性偏移
    wisdom_offset = 0
    power_offset = -0.3
    openness_offset = 0.3
    charm_offset = 0
    # 特质
    height = 170
    weight = 65


class Elf(RaceBase):
    name: str = "Elf"
    # 基础属性改动
    lifetime = 100
    pregnancy = 20
    sex = True
    militancy_offset = 0
    mating_offset = 0
    marry_offset = 0
    fertility_offset = 0
    # 属性偏移
    wisdom_offset = 0.1
    power_offset = 0.1
    openness_offset = -0.3
    charm_offset = 0.4
    # 特质
    height = 185
    weight = 70


class Dwarf(RaceBase):
    name: str = "Dwarf"
    # 基础属性改动
    lifetime = 60
    pregnancy = 4
    sex = True
    militancy_offset = 0
    mating_offset = 0
    marry_offset = 0
    fertility_offset = 0
    # 属性偏移
    wisdom_offset = 0.1
    power_offset = 0.4
    openness_offset = -0.5
    charm_offset = -0.3
    # 特质
    height = 130
    weight = 60


class Orc(RaceBase):
    name: str = "Orc"
    # 基础属性改动
    lifetime = 60
    pregnancy = 8
    sex = True
    militancy_offset = 0
    mating_offset = 0
    marry_offset = 0
    fertility_offset = 0
    # 属性偏移
    wisdom_offset = -0.3
    power_offset = 0.4
    openness_offset = 0
    charm_offset = -0.2
    # 特质
    height = 200
    weight = 85
