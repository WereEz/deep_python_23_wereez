class LRUCache:
    def __init__(self, limit=42):
        if not isinstance(limit, int):
            raise TypeError
        if limit <= 0:
            raise ValueError
        self.limit = limit
        self.dct = {}

    def get(self, key):
        if key not in self.dct:
            return None
        self.dct[key] = self.dct.pop(key)
        return self.dct[key]

    def set(self, key, value):
        if key in self.dct:
            self.dct.pop(key)
        if self.limit <= len(self.dct):
            self.dct.pop(next(iter(self.dct)))
        self.dct[key] = value
