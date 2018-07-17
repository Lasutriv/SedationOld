import time

# A collection of classes and functions to help debug the game code. When naming in the program, use DEV_xxx_xxx for the class and function names.


class TimeHandler(object):

    def __init__(self):
        self.on = True
        self.print = False
        self.time = 0
        self.time_board = []

    def clock_start(self):
        """
        A function to start the clock for possibly timing such as functions.

        @return: none
        @rtype: none
        """
        if self.on is True:
            self.time = time.clock()

    def clock_stop(self):
        if self.on is True:
            self.time = time.clock() - self.time

    def clock_stop_add(self):
        if self.on is True:
            self.clock_stop()
            self.clock_board_add()
            self.clock_clear()

    def clock_clear(self):
        self.time = 0

    def clock_on(self, on: bool):
        if on is True or on is False:
            self.on = on

    def clock_board_add(self):
        if len(self.time_board) < 50:
            self.time_board.append(str(self.time))
        else:
            self.clock_on(False)
            self.print = True

    def clock_board_clear(self):
        self.time_board = []

    def clock_board_print(self):
        if self.print is True:
            total = 0.0
            counter = 1
            for clock_time in self.time_board:
                # Prints individual clock times
                # print(str(counter) + ': ' + clock_time)
                total += float(clock_time)
                counter += 1
            average = total / float(len(self.time_board))
            print('Total: ' + str(total))
            print('Quantity: ' + str(float(len(self.time_board))))
            print('Average: ' + str(average))
            self.print = False