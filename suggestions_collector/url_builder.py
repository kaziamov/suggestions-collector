from itertools import chain


class UrlBuilder:
    def get_tags(self, path='input_urls.txt'):
        with open(path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        new_tags = chain(*[line.split(',') for line in lines])
        self.tags = [tag.strip() for tag in new_tags]
        return self

    def make_url(self):
        self.urls = [tag.replace(' ', '-').lower() for tag in self.tags]
        return self

    def print_urls(self):
        print(*self.urls)


if __name__ == "__main__":
    builder = UrlBuilder()
    builder.get_tags().make_url().print_urls()