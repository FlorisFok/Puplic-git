class Room(object):
    """
    Representation of a room in Adventure
    """

    def __init__(self, id, name, description):
        """
        Initializes a Room
        """
        self.id = id
        self.name = name
        self.description = description
        self.direction = []

    def __str__(self):
        return self.name

    def add_route(self, direction, item_req):
        """
        Adds a given direction and the connected room to our room object.
        """
        self.direction.append((direction, item_req))

    def is_connected(self, direction, inventory):
        """
        Checks whether the given direction has a connection from a room.
        Returns a boolean.
        """

        direction_pos = []

        # Searches possible moves
        for dir_tuple in self.direction:
            direction_pos.append(dir_tuple[0][0])

        # Checks if the prefered move is in de posible moves
        if direction in direction_pos:
            return True
        return False