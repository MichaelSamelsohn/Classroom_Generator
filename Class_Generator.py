"""
Author: Michael Samelsohn (advised by Eleonora Levin), 25/05/22.
"""

# Imports #
import math
import random

from Pupils import PUPIL_LIST, Pupil
from Logging import Logger
import os

# Logger #
log = Logger(module=os.path.basename(__file__), file_name=None)

# Constants #
CLASSROOM_SEATINGS = 10
MAX_NUMBER_OF_ITERATIONS = 200


class Table:
    """
    Class that represents a table (node). Each table has two pupils seated on it (at most).
    Each table is designated by its row and column positions in the class.
    """

    def __init__(self, row, col):
        self.next_table = None

        self.row = row
        self.col = col

        self.left_seat = None
        self.right_seat = None


class Classroom:
    """
    Class that represents a classroom (linked list). A classroom consists of pupils and tables (the amount is compatible
    with the pupil list).
    """

    def __init__(self, pupil_list: list[Pupil]):
        self.pupil_list = pupil_list

        self.status = True  # Status of the generation. Assuming successful.

        self.class_width = math.ceil(math.sqrt(len(pupil_list) / 2))
        self.head_table = Table(row=0, col=0)  # 'Head' table.
        traversal_table = self.head_table
        for row in range(self.class_width):
            for col in range(self.class_width):
                traversal_table.next_table = Table(row=row, col=col)
                traversal_table = traversal_table.next_table

        self.head_table = self.head_table.next_table  # To avoid two head tables.

    def __front_row_precedence(self):
        front_row_precedence_list = []
        for pupil in self.pupil_list:
            if pupil.front_row_precedence is True:
                front_row_precedence_list.append(pupil)
        return front_row_precedence_list

    def __rest_of_class_list(self, front_row_precedence_list):
        # Build a list of pupils with front row precedence.
        rest_of_class_list = []
        for pupil in self.pupil_list:
            if pupil not in front_row_precedence_list:
                rest_of_class_list.append(pupil)
        return rest_of_class_list

    def __are_pupils_compatible(self, pupil1, pupil2):
        for bad_pupil in pupil2.list_of_bad_people:
            if bad_pupil == pupil1.name:
                return False

        for bad_pupil in pupil1.list_of_bad_people:
            if bad_pupil == pupil2.name:
                return False

        return True

    def __seat_listed_pupils(self, current_table, list_of_pupils):
        """
        Traverse from the current table, pick pupils randomly and seat them (while asserting they can sit together).
        Once a table is full, move to the next one and repeat until no pupils are left in the list.

        :param current_table: The table currently vacant (even partially).
        :param list_of_pupils: The lst of pupils to be seated.
        :return: The table after all the listed pupils were seated.
        """

        iterations_counter = 0  # Used for counting the iterations.
        while len(list_of_pupils) > 0 and iterations_counter < MAX_NUMBER_OF_ITERATIONS:  # List is not empty.
            # Pick a random pupil.
            random_pupil_index = random.randint(0, len(list_of_pupils) - 1)
            pupil = list_of_pupils[random_pupil_index]
            if current_table.right_seat is None:
                # Table is empty, seat the pupil.
                current_table.right_seat = pupil
                list_of_pupils.pop(random_pupil_index)  # Remove the pupil (he is seated).
            elif current_table.left_seat is None:
                # Table has one pupil seated on the right.
                # Checking if seated pupil is not on bad people list.
                if self.__are_pupils_compatible(pupil1=current_table.right_seat, pupil2=pupil):
                    # Pupils can seat together, seat the pupil.
                    current_table.left_seat = pupil
                    list_of_pupils.pop(random_pupil_index)  # Remove the pupil (he is seated).
                    current_table = current_table.next_table  # Table is full, move to the next one.

            iterations_counter += 1

        # Asserting that all pupils were seated.
        if len(list_of_pupils) > 0:
            # Not all pupils were seated, the generation process failed.
            self.status = False

        return current_table

    def generate_class_seating(self):
        """
        Seat all the pupils in the classroom list.
        The seating process is done in turns, each time with the next precedence list.
        """

        current_table = self.head_table

        # First seat all the people with precedence.
        front_row_precedence_list = self.__front_row_precedence()
        current_table = self.__seat_listed_pupils(current_table=current_table, list_of_pupils=front_row_precedence_list)

        # Next, seat the rest of the class.
        rest_of_class_list = self.__rest_of_class_list(front_row_precedence_list=self.__front_row_precedence())
        current_table = self.__seat_listed_pupils(current_table=current_table, list_of_pupils=rest_of_class_list)

    def print_classroom_seating(self):
        """
        Prepare a string with the generated classroom seating arrangement.

        :return: String with the classroom seating arrangement.
        """

        if self.status is False:
            # Generation process failed.
            return None

        traversal_table = self.head_table
        classroom_print = ""  #
        try:
            for row in range(self.class_width):
                classroom_print += "\n\n"
                for col in range(self.class_width):
                    classroom_print += f"{traversal_table.left_seat.name} - {traversal_table.right_seat.name}    "
                    traversal_table = traversal_table.next_table
        except AttributeError:
            return classroom_print

        return classroom_print


if __name__ == "__main__":
    list_of_classroom_seating_prints = []

    for classroom_seating in range(CLASSROOM_SEATINGS):
        classroom = Classroom(pupil_list=PUPIL_LIST)
        classroom.generate_class_seating()
        list_of_classroom_seating_prints.append(classroom.print_classroom_seating())

    list_of_classroom_seating_prints = list(filter(None, list_of_classroom_seating_prints))
    for classroom_seating_print in list_of_classroom_seating_prints:
        log.info(classroom_seating_print)
        log.debug("\n")
    log.info(f"Successful classroom seating arrangements found - {len(list_of_classroom_seating_prints)}")
