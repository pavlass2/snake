#!/usr/bin/python


class KeyCash:
    # each element is a list where first element is the key and the second one is True/False if it was already used
    __last_command = []

    def add_command(self, command):
        self.__last_command.append([command, False])

    def get_last_command(self):
        # if we have more than 1 command in the cash, we have to remove the already used
        if len(self.__last_command) > 1:
            # iterate through all of them
            counter = 0
            while counter < len(self.__last_command):
                # if the command was already used
                if self.__last_command[counter][1]:
                    # delete it
                    del self.__last_command[counter]
                counter += 1
        # mark command as used and return it
        self.__last_command[0][1] = True
        return self.__last_command[0][0]

    def reset(self):
        self.__last_command.clear()
