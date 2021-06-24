from assistance import *
import pandas as pd


class PopulationChecker:
    def __init__(self, game):
        self.game = game
        self.yearly_record: list = []
        self.total_data: dict = []
        # yearly record
        self.marry_num_yearly: int = 0
        self.pregnant_num_yearly: int = 0
        self.abortion_num_yearly: int = 0
        self.born_num_yearly: int = 0
        self.death_num_yearly: int = 0
        self.make_love_num_yearly: int = 0

        self.ml_diff_race_yearly: int = 0
        self.marry_diff_race_yearly: int = 0
        self.ml_diff_tribe_yearly: int = 0
        self.marry_diff_tribe_yearly: int = 0

    def yearly_zeroing(self):
        self.marry_num_yearly = 0
        self.pregnant_num_yearly = 0
        self.abortion_num_yearly = 0
        self.born_num_yearly = 0
        self.death_num_yearly = 0
        self.make_love_num_yearly: int = 0

        self.marry_diff_race_yearly = 0
        self.marry_diff_tribe_yearly = 0

    def record_yearly_data(self):
        params = dict()
        params['纪年'] = self.game.years
        params['总数'] = len(self.game.get_all_roles())
        params['出生数'] = self.born_num_yearly
        params['死亡数'] = self.death_num_yearly
        params['成婚对数'] = self.marry_num_yearly
        params['怀孕数'] = self.pregnant_num_yearly
        params['流产数'] = self.abortion_num_yearly
        params['交媾数'] = self.make_love_num_yearly
        params['与异种结婚数'] = self.marry_diff_race_yearly
        params['与异族结婚数'] = self.marry_diff_tribe_yearly

        self.yearly_record.append(params)

    def record_total_data(self):
        params = dict()
        params['纪年'] = self.game.years
        params['总数'] = len(self.game.get_all_roles())
        params['出生数'] = sum([x['出生数'] for x in self.yearly_record])
        params['死亡数'] = sum([x['死亡数'] for x in self.yearly_record])
        params['成婚对数'] = sum([x['成婚对数'] for x in self.yearly_record])
        params['怀孕数'] = sum([x['怀孕数'] for x in self.yearly_record])
        params['流产数'] = sum([x['流产数'] for x in self.yearly_record])
        params['交媾数'] = sum([x['交媾数'] for x in self.yearly_record])
        params['总流产率'] = params['流产数'] / params['怀孕数']

        params['与异种结婚数'] = sum([x['与异种结婚数'] for x in self.yearly_record])
        params['与异族结婚数'] = sum([x['与异族结婚数'] for x in self.yearly_record])

        self.total_data = params

    def get_population_growth_rate(self):
        pass

    def round_check(self):
        self.record_yearly_data()
        self.yearly_zeroing()

    def save_data(self):
        base_path = os.getcwd()
        folder = base_path + '\\' + 'RECORDS'
        if not os.path.exists(folder):
            os.makedirs(folder)

        df = pd.DataFrame(self.yearly_record)
        df.to_csv(folder + '\\population_record.csv', index=False)
        save(self.total_data, 'RECORDS', 'population_record.txt')
