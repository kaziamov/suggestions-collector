from itertools import chain
from main import Collector
from collections import Counter


class Cleaner:

    def __init__(self) -> None:
        self.tags = []
        self.counted_tags = []
        self.filtered_tags = []
        self.target_keywords = []

    def get_tags(self, path='input_tags.txt'):
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        new_tags = chain(*[line.split(',') for line in lines])
        self.tags = [tag.strip() for tag in new_tags]
        return self

    def count_tags(self):
        self.counted_tags = Counter(self.tags)
        return self

    def filter_tags(self):
        # self.filtered_tags = [key for key, value in dict(self.counted_tags).items() if value > 1]
        self.filtered_tags = self.counted_tags.keys()
        # self.filtered_tags = [keyword for keyword in filtered_tags if keyword in self.target_keywords]
        return self

    def print_tags(self):
        print(*self.filtered_tags, sep=',')
        return self

    def print_hashtags(self):
        tags = [tag.replace(' ', '') for tag in self.filtered_tags]
        print(*tags, sep=', #')
        return self




if __name__ == "__main__":
    c = Cleaner().get_tags().count_tags().filter_tags().print_tags().print_hashtags()