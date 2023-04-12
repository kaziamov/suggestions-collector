class Parsing():

    def __init__(self, queries, parsing_methods):
        self.queries = queries
        self._parsing_methods = parsing_methods
        self.collect_values = {}


    def collect(self):
        for query in self.queries:
            self.collect_values.setdefault(query, [])
            for method in self._parsing_methods:
                self.collect_values.extend(method.collect(query))

    def collect_old(self):
        # self.collect_list = itertools.chain.from_iterable(map(self._get_request, self.queries))
        pass

    def reset(self):
        self.queries = {}
