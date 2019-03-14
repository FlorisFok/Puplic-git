class Item(object):
    """
    Representation of a item in Adventure
    """

    def __init__(self, initial_loc, name, description):
        self.name = name
        self.initial_loc = initial_loc
        self.description = description
        self.location = initial_loc

    def __str__(self):
        '''
        Short introduction of the item
        '''
        return f"{self.name}: {self.description}"