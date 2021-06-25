import random
from race import *
from constants import *
from logger import logger
import os


def get_random_race() -> str:
    return random.choice(TRIBES_LIST)


def get_random_name() -> str:
    word_list = [chr(i) for i in range(97, 123)]
    name = ''.join([random.choice(word_list) for i in range(random.randint(3, 10))])
    return name


def get_random_land_name() -> str:
    return random.choice(list(map(lambda x: str(x), range(10000, 99999))))


def get_mean_range(*value, per_range: float = 0.1) -> float:
    """
    返回几个数均值的随机范围
    :param value: 值关键字
    :param per_range: 范围
    :return: 均值在一定范围内的偏移随机数
    """
    return sum(value) / len(value) * (1 + random.uniform(-per_range, per_range))


def get_offset(value, offset) -> float:
    return value * (1 + offset)


def normalvariate(mu, sigma=2):
    return random.normalvariate(mu, sigma)


def offset_by_age(value, offset_list: list, lifetime, age):
    try:
        age = age if age < lifetime else lifetime - 1
        return retain_demical(value * (1 + offset_list[int(age / (lifetime / len(offset_list)))]))
    except:
        logger.error("value{},lifetime{},age{}".format(value, lifetime, age))
        return 9999


def retain_demical(value, n=3):
    x = 10 ** n
    return int(value * x) / x


def get_mixture_race(mix1: dict, mix2: dict) -> dict:
    mix1 = dict(zip(mix1, map(lambda x: x / 2, mix1.values())))
    mix2 = dict(zip(mix2, map(lambda x: x / 2, mix2.values())))
    result = dict()
    for key in mix1.keys() | mix2.keys():
        result[key] = sum([d.get(key, 0) for d in (mix1, mix2)])
    return result


def save(params: dict, folder, file):
    base_path = os.getcwd()
    folder = base_path + '\\' + folder
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(folder + '\\' + file, 'a') as file_obj:
        for key, value in params.items():
            if isinstance(value, dict):
                text = []
                for sub_key, sub_value in value.items():
                    text.append(sub_key + ': ' + str(sub_value))
                text = ', '.join(text)
                file_obj.write(key + ': ' + text + '\n')
            elif isinstance(value, list):
                file_obj.write(key + ': ' + ', '.join(value) + '\n')
            else:
                file_obj.write(key + ': ' + str(value) + '\n')


def is_happened_by_pro(pro):
    pro = pro if pro <= 1 else 1
    pro = int(pro * 1000)
    pool = [1 for i in range(pro)] + [0 for i in range(1000 - pro)]
    flag = random.choice(pool)
    return flag


def act_by_pro(pro, func, *args):
    flag = is_happened_by_pro(pro)
    if flag:
        func(*args)


if __name__ == "__main__":
    aa = [-0.99, -0.9, -0.6, -0.2, 0, 0, 0, 0, 0, -0.1, -0.2, -0.2, -0.3, -0.3, -0.4, -0.4, -0.5, -0.5,
          -0.6, -0.7]
    for i in range(0, 100, 2):
        a = offset_by_age(50, aa, 100, i)
        print('years: ' + str(i) + ', pro: ' + str(a))
