import random
import os


class NameGenerator:
    def __init__(self):
        base_path = 'name_generator'
        self.first_name_male_path = base_path + '\\' + r'first_name_male.txt'
        self.first_name_female_path = base_path + '\\' + 'first_name_female.txt'
        self.last_name_path = base_path + '\\' + 'last_name.txt'
        self.first_name_male_list = []
        self.first_name_female_list = []
        self.last_name_list = []
        self.read_files()

    def read_files(self):
        with open(self.first_name_male_path) as f1:
            name_list = f1.read().splitlines()
            self.first_name_male_list.extend(name_list)
        with open(self.first_name_female_path) as f2:
            name_list = f2.read().splitlines()
            self.first_name_female_list.extend(name_list)
        with open(self.last_name_path) as f3:
            name_list = f3.read().splitlines()
            self.last_name_list.extend(name_list)

    def get_random_last_name(self):
        return random.choice(self.last_name_list)

    def get_random_first_name(self, gender):
        if gender == 'male':
            return random.choice(self.first_name_male_list)
        elif gender == 'female':
            return random.choice(self.first_name_female_list)
        else:
            return random.choice(self.first_name_male_list + self.first_name_female_list)

    def get_random_name(self, gender, last_name: str = ''):
        last_name = last_name if last_name else self.get_random_last_name()
        return self.get_random_first_name(gender) + ' ' + last_name
