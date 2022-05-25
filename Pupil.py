"""
Author: Michael Samelsohn (advised by Eleonora Levin), 25/05/22.
"""


class Pupil:
    """
    Class that represents a pupil. Each pupil has three attributes:
        * Name (identifier).
        * Front row precedence - True if pupil wears glasses (or has trouble seeing), makes a lot of noise and has to be
          under monitoring, False otherwise.
        * List of pupils he shouldn't be seated with due to bad relations, or they make noise together.
    """

    def __init__(self, name: str, front_row_precedence: bool, list_of_bad_people: list):
        self.name = name
        self.front_row_precedence = front_row_precedence
        self.list_of_bad_people = list_of_bad_people
