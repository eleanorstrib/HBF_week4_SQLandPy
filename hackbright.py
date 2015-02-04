import sqlite3

CONN = sqlite3.connect('hackbright.db')
DB = CONN.cursor()


def get_student_by_github(github):
    query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
    DB.execute(query, (github,))
    row = DB.fetchone()
    print """\
Student: %s %s
Github account: %s"""%(row[0], row[1], row[2])


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()


def make_new_student(first_name, last_name, github):
    query = """INSERT into Students values(?, ?, ?)"""
    DB.execute(query,(first_name, last_name, github))

    CONN.commit()
    print "Successfully added student %s %s" % (first_name, last_name)


def projects_by_title(title):
    query = """SELECT description, max_grade FROM Projects WHERE title = ?"""
    DB.execute(query, (title,))
    row = DB.fetchone()
    print """\
Description: %s
Max Grade: %s"""%(row[0], row[1])


def add_a_project(title, description, max_grade):
    query = """INSERT into Projects (title, description, max_grade)
                values (?, ?, ?)"""
    DB.execute(query,(title, description, max_grade))
    
    CONN.commit()
    print """\
Successfully added a project with the following parameters:
Title: %s
Description: %s
Max Grade: %s""" % (title, description, max_grade)


def get_student_grade(github, project_title):
    query = """SELECT s.first_name, s.last_name, g.grade, p.max_grade
                FROM Students AS s 
                LEFT JOIN Grades AS g ON (s.github=g.student_github)
                JOIN Projects AS p ON (g.project_title=p.title)
                WHERE s.github = ? AND g.project_title= ?"""
    DB.execute(query, (github, project_title))
    row = DB.fetchone()
    print """\
    %s %s has a grade of %s out of a possible %s on that project.""" %(row[0], row[1], row[2], row[3])

def give_student_grade(github,project,grade):
    query = """INSERT INTO Grades
                VALUES(?, ?, ?)"""
    DB.execute(query, (github, project, grade))
    CONN.commit()
    print """\
    Successfully assigned student with Github ID %s a grade of %s for the %s project."""%(github, grade, project)


def show_all_grades(github):
    query = """SELECT s.first_name, s.last_name, g.grade, g.project_title
                FROM Students AS s
                LEFT JOIN Grades AS g ON(s.github=g.student_github)
                WHERE s.github = ?"""
    DB.execute(query,(github,))
    row = DB.fetchall()
    for tuple in row:
        print "%s %s has a grade of %s on the %s project." % (tuple[0], tuple[1], tuple[2], tuple[3])


def main():
    connect_to_db()
    command = None
    while command != "quit":
        input_string = raw_input("HBA Database> ")
        tokens = input_string.split(",")
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            get_student_by_github(*args) 
        elif command == "new_student":
            make_new_student(*args)
        elif command == "project_info":
            projects_by_title(*args)
        elif command == "new_project":
            add_a_project(*args)
        elif command == "project_grade":
            get_student_grade(*args)
        elif command == "give_grade":
            give_student_grade(*args)
        elif command =="show_grades":
            show_all_grades(*args)
        elif command == "quit":
            print "Goodbye!"
        else:
            print "That command is not available -- please try again"

    CONN.close()

if __name__ == "__main__":
    main()
