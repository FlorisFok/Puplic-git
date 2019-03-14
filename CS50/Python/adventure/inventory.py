class Inventory(object):
    """
    Representation of a inventory in Adventure
    """

    def __init__(self, items={}):
        self.item_dict = items

    def __str__(self):
        '''
        IF strinf is requested, returns the stuff the inventory contains
        '''
        message = 'The Invetory contains: \n'
        for i, item in enumerate(list(self.item_dict.keys())[1:]):
            message += f"{i+1}. {str(self.item_dict[item])}\n"

        if list(self.item_dict.keys())[1:] == []:
            message = "Your inventory is empty"
        return message

    def locations(self):
        """
        Checks location of items and returns list of (location and name).
        In this way we know when we need to look for a item
        """
        ids = []
        for key in self.item_dict.keys():
            if key == 'None':
                continue
            ids.append((int(self.item_dict[key].initial_loc),
                        self.item_dict[key]))
        return ids

    def add(self, item):
        """
        Adds item to inventory
        """
        self.item_dict[item.name] = item

    def remove(self, loc):
        """
        removes item from inventory
        """
        return self.item_dict.pop(loc)

