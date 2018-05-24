class ActionProfile(dict):
    """
    basically a map that allows to access its keys
    via "." notation, i.e. map.x instead of map['x']
    """
    def add(self, name, action):
        self.__setitem__(name, action)

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(ActionProfile, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(ActionProfile, self).__delitem__(key)
        del self.__dict__[key]