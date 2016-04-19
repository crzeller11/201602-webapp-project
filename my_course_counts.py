from os import chdir
from os.path import dirname, realpath

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# FIXME write your app below

class Course_Info:
    def __init__(self, year, season, department, course_num, section_title, units, professor, schedule, core,
                 total_seats, enrolled, reserved, reserved_open, waitlisted):
        self.year = year
        self.season = season
        self.department = department
        self.course_num = course_num
        self.section_title = section_title
        self.units = units
        self.professor = professor
        self.schedule = schedule
        self.core = core
        self.total_seats = total_seats
        self.enrolled = enrolled
        self.reserved = reserved
        self.reserved_open = reserved_open
        self.waitlisted = waitlisted

def get_data():
    course_data = []
    with open('counts.tsv') as file:
        for line in file.read().splitlines():
            year, season, department, course_num, section_title, units, professor, schedule, core, total_seats, \
            enrolled, reserved, reserved_open, waitlisted = line.split('\t')
            course_data.append(Course_Info(year, season, department, course_num, section_title, units, professor,
            schedule, core, total_seats, enrolled, reserved, reserved_open, waitlisted))
    return course_data

# check the course_info class and just see if thats the right thing to do and then check the get_data function. I don't
# think the list course_data needs to b sorted like in did in the flask lab, because we aren't searching for anything in
# particular like we were before.

@app.route('/course_counts')
def view_root():
    return render_template('base.html')


# The functions below lets you access files in the css, js, and images folders.
# You should not change them unless you know what you are doing.

@app.route('/images/<file>')
def get_image(file):
    return send_from_directory('images', file)

@app.route('/css/<file>')
def get_css(file):
    return send_from_directory('css', file)

@app.route('/js/<file>')
def get_js(file):
    return send_from_directory('js', file)

if __name__ == '__main__':
    chdir(dirname(realpath(__file__)))
    app.run(debug=True)
