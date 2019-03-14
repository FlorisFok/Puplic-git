"""
THE ADVENTURE GAME,

please enter txt files in correct format
enjoy the game

for help, enter help in the game

Floris Fok
"""


from room import Room
from item import Item
from inventory import Inventory
import sys


WINNING_ROOM = 77


class Adventure():
    """
    This is your Adventure game class. It should contains
    necessary attributes and methods to setup and play
    Crowther's text based RPG Adventure.
    """

    def __init__(self, game):
        """
        Create rooms and items for the appropriate 'game' version.
        """
        # Check50 compatability, checks data folder in two destinations
        try:
            self.rooms = self.load_rooms(f"data/{game}Rooms.txt")
            self.items = self.load_items(f"data/{game}Items.txt")
        except:
            self.rooms = self.load_rooms(f"../data/{game}Rooms.txt")
            self.items = self.load_items(f"../data/{game}Items.txt")

        # Set up rooms, items and inventorys
        self.current_room = self.rooms[1]
        self.inv_computer = Inventory(self.items)
        self.inv_human = Inventory({'None': Item('None', 'None', 'None')})

    def __str__(self):
        """
        returns a string of the help text written in another file.
        """
        return ("THIS MIGHT HELP:\n"
                "You can move by typing directions such as EAST/WEST/IN/OUT\n"
                "QUIT quits the game.\n"
                "HELP prints instructions for the game.\n"
                "INVENTORY lists the item in your inventory.\n"
                "LOOK lists the complete description of the room and its "
                "contents.\n"
                "TAKE <item> take item from the room.\n"
                "DROP <item> drop item from your inventory\n")

    def load_rooms(self, filename):
        """
        Load rooms from filename.
        Returns a dictionary of 'id' : Room objects.
        """
        # First we parse all the data we need to create the rooms with.
        # All parsed lines of data are saved to rooms_data.
        rooms_data = []
        with open(filename, "r") as f:
            room_data = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    room_data.append(line.strip())
                # A blank newline signals all data of a single room is parsed.
                else:
                    rooms_data.append(room_data)
                    room_data = []
        # Append a final time, because the files do not end on a blank newline.
        rooms_data.append(room_data)

        # Create room objects for each set of data we just parsed.
        rooms = {0: Room(0, 'Game over', 'You died or won')}
        for room_data in rooms_data:
            id = int(room_data[0])
            name = room_data[1]
            description = room_data[2]

            # Initialize a room object and put it in a dictionary with its
            # id as key.
            room = Room(id, name, description)
            rooms[id] = room

        # Add routes to each room we've created with the data from each set
        # we have parsed earlier.
        for room_data in rooms_data:
            id = int(room_data[0])
            # We split to connections into a direction and a room_id.
            connections = room_data[4:]
            connections = [connection.split() for connection in connections]
            # Here we get the current room object that we'll add routes to.
            room = rooms[id]
            items = []
            for connection, target_room_id in connections:
                try:
                    room_id = int(target_room_id)
                    item_req = 'None'
                except:
                    room_id = target_room_id.split('/')[0]
                    item_req = target_room_id.split('/')[1]
                room.add_route((connection, room_id), item_req)

        return rooms

    def load_items(self, filename):
        """
        Load items from filename.
        Returns a dictionary of item_name: item objects.
        """
        # First we parse all the data we need to create the items with.
        # All parsed lines of data are saved to data.
        datas = []
        with open(filename, "r") as f:
            data = []
            for line in f:
                # When there is no blank newline it means there's still data.
                if not line == "\n":
                    data.append(line.strip())
                # A blank newline signals all data of a single item is parsed.
                else:
                    datas.append(data)
                    data = []
        # Append a final time, because the files do not end on a blank newline.
        datas.append(data)

        # Create item objects for each set of data we just parsed.
        items = {}
        for data in datas:
            name = data[0]
            description = data[1]
            room_id = data[2]

            # Initialize a item object and put it in a dictionary with its
            # id as key.
            item = Item(room_id, name, description)
            items[name] = item

        return items

    def game_over(self):
        """
        Check if the game is over.
        Returns a boolean.
        """
        if self.current_room.id == 0:
            print("Game Over")
            return True
        return False

    def move(self, direction):
        """
        Moves to a different room in the specified direction.
        """
        # First looks at the items you have
        items_pos = self.inv_human.item_dict.keys()

        # Find the required items
        items_req = []
        rooms_pos = []
        for dir_tuple in self.current_room.direction:
            # Safe info about relevant room
            if dir_tuple[0][0] == direction.upper():
                items_req.append(dir_tuple[1])
                rooms_pos.append(int(dir_tuple[0][1]))

        # Reverse room, this will make it easier to override the new_room
        new_room = -1
        items_req.reverse()
        rooms_pos.reverse()

        # Checks if all items are available for a direction, other wise moves to
        # Room without item (is always at index 0)
        for i, room in enumerate(rooms_pos):
            if items_req[i] in items_pos:
                new_room = room
            else:
                # When mutliple items are required, but not there: overwrite room
                if new_room == room:
                    new_room = rooms_pos[0]

        # If a room+item matches, move and return True
        if new_room > -1:
            self.current_room = self.rooms[new_room]
            return True
        else:
            return False

    def print_tekst(self, room_num):
        """
        Prints the basic info we need to print evry time things change
        """
        print("______________________________________________________")
        print(self.current_room)
        print(self.current_room.description)
        print("Room #" + str(room_num))
        # Searches for locations of the items.
        try:
            loc, items = zip(*self.inv_computer.locations())
        except:
            loc = []
        # if the room contains a item, print it.
        if room_num in loc:
            print("Found an item!")
            print(items[loc.index(room_num)])
        else:
            pass

    def item_drop(self, commands, room_num):
        """
        Moves item from player inventory to computer
        """
        com = self.inv_computer.item_dict
        hum = self.inv_human.item_dict
        # If the item is n your inventory, you can drop it
        if commands[1] in list(hum.keys()):
            # Transferres item between inventories
            item = self.inv_human.remove(commands[1])
            self.inv_computer.add(Item(room_num, item.name, item.description))
            # Calls it by name if you can drop it
            print(commands[1]+" dropped")
            return True
        # Tells you if you cant drop it
        print("No such item")
        return False

    def pick_item(self, commands, room_num):
        """
        Moves item from computer inventory to player
        """
        com = self.inv_computer.item_dict
        hum = self.inv_human.item_dict
        # If the item is there where you currently are, you can pick it up
        try:
            if int(com[commands[1]].location) == int(room_num):
                self.inv_human.add(self.inv_computer.remove(commands[1]))
                print(commands[1]+" taken")
                return True
            else:
                print("No such item")
                return False
        except:
            print("No such item")
            return False

    def play(self):
        """
        Play an Adventure game
        """
        print(f"Welcome, to the Adventure games.\n"
              "May the randomly generated numbers be ever in your favour.\n")

        tries = 0
        # Prompt the user for commands until they've won the game.
        while not self.game_over():

            # Gives room number
            room_num = int(self.current_room.id)

            # prints tekst if things have changed
            if tries == 0:
                self.print_tekst(room_num)
            if self.current_room.direction[0][0][0] == 'FORCED':
                self.move('FORCED')
                continue
            else:
                # Gets players input and splits the commands up
                command = input("> ").upper()
                commands = command.split(" ")

            # Checks if it's a possible move.
            if self.current_room.is_connected(commands[0], self.inv_human) and len(commands) == 1:
                tries = 0
                if not self.move(commands[0]):
                    tries += 1
                    print("Invalid command.")

            # If you ask for help, prints help
            elif commands[0] == 'HELP':
                print(self.__str__())
                tries = 0

            # Ends game, when you enter quit
            elif commands[0] == 'QUIT':
                print("Thanks for playing!")
                break

            # Reprints the description
            elif commands[0] == 'LOOK':
                print(self.current_room.description)
                tries = 0

            # Makes you pick an item
            elif commands[0] == 'TAKE':
                if len(commands) > 1:
                    if self.pick_item(commands, room_num):
                        tries = 0
                        continue
                tries += 1
                print("Invalid command.")

            # Makes you drop an item
            elif commands[0] == "DROP":
                if len(commands) > 1:
                    if self.item_drop(commands, room_num):
                        tries = 0
                        continue
                tries += 1
                print("Invalid command.")

            # Shows items in inventory
            elif commands[0] == "INVENTORY":
                print(self.inv_human)
                tries += 1

            # If all is false: you did something wrong
            else:
                print("Invalid command.")
                tries += 1

            # Checks if you've won
            if self.current_room.id == WINNING_ROOM:
                print("You have collected all the treasures and are admitted"
                      "to the Adventurer's Hall of Fame.  Congratulations!")
                break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)
    elif sys.argv[1] == "Tiny" or sys.argv[1] == "Small" or sys.argv[1] == "Crowther":
        adventure = Adventure(sys.argv[1])
        adventure.play()
    else:
        sys.exit(1)

