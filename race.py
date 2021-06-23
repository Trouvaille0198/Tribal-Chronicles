class RaceBase:
    lifetime: int = 100
    pregnancy: int = 4
    sex: bool = True
    militancy: float = 0
    mating_probability: float = 50
    marry_probability: float = 20

    wisdom: float = 50
    power: float = 50
    fertility: float = 50
    openness: float = 50
    charm: float = 50

    height: float = 170
    weight: float = 65


class Humankind(RaceBase):
    name: str = "Humankind"
    # 基础属性改动
    lifetime = 70
    lifetime_offset = 0.3
    pregnancy = 3
    militancy_offset = 0
    mating_offset = 0
    marry_offset = 0
    # 属性偏移
    wisdom_offset = 0.1
    power_offset = -0.2
    fertility_offset = 0.3
    openness_offset = 0.3
    charm_offset = 0
    # 特质
    height_offset = 0
    weight_offset = 0
