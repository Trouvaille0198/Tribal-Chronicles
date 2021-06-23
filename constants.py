import numpy as np

HEIGHT_OFFSET_BY_AGE = list(map(lambda x: x / 50, range(-50, 0, 1))) + [0 for i in range(190)] + list(
    map(lambda x: x / 100, range(0, -50, -1)))
WEIGHT_OFFSET_BY_AGE = list(map(lambda x: x / 50, range(-50, 0, 1))) + [0 for j in range(190)] + list(
    map(lambda x: x / 100, range(0, -50, -1)))
ABILITY_OFFSET_BY_AGE = list(map(lambda x: x / 50, range(-50, 0, 1))) + [0 for k in range(190)] + list(
    map(lambda x: x / 100, range(0, -50, -1)))
MATING_OFFSET_BY_AGE = list(map(lambda x: x / 50, range(-50, 0, 1))) + [0 for k in range(100)] + list(
    map(lambda x: x / 100, range(0, -100, -1)))
MARRY_OFFSET_BY_AGE = list(map(lambda x: x / 50, range(-50, 0, 1))) + [0 for k in range(100)] + list(
    map(lambda x: x / 100, range(0, -100, -1)))
