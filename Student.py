class Student:
    name = " "
    grade = 0
    lesson_num = 0
    lesson_total = 0
    id = 0

    def __init__(self, _name, _grade,_id):
        self.name = _name
        self.grade = _grade
        self.id = _id


class Teacher:
    name = " "
    subject_list = []
    group_list = []
    student_list = []

    def __init__(self):
        self.name = " "

    def set_name_surname(self, _name):
        self.name = _name

    def add_subject(self, _subject):
        self.subject_list.append(_subject)

    def get_students(self):
        return self.student_list
