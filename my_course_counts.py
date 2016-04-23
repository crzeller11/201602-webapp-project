from os import chdir
from os.path import dirname, realpath

from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)

# FIXME write your app below

class Course_Info:
    def __init__(self, year, season, department, course_num, section, title, units, professor, schedule, core,
                 total_seats, enrolled, reserved, reserved_open, waitlisted):
        self.year = year
        self.season = season
        self.department = department
        self.course_num = course_num
        self.section = section
        self.title = title
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
            year, season, department, course_num, section, title, units, professor, schedule, core, total_seats, \
            enrolled, reserved, reserved_open, waitlisted = line.split('\t')
            course_data.append(Course_Info(year, season, department, course_num, section, title, units, professor,
            schedule, core, total_seats, enrolled, reserved, reserved_open, waitlisted))
    return course_data

# how do we know when we have that weird indexing issue that we have to deal with?


# check the course_info class and just see if that's the right thing to do and then check the get_data function. I don't
# think the list course_data needs to be sorted like in did in the flask lab, because we aren't searching for anything in
# particular like we were before.

'''
THings we need:
HTML file that displays results (filtered_page)
Design, what should entire website looks like, what should CSS look like? What should whole design look like
'''


@app.route('/')
def view_root():
    return render_template('base.html')



@app.route('/results') # This function needs to have a loop that acquires the right information to be displayed on the
# figure out the URL would be for the selections
def view_course_info():
    year = request.args.get('year')
    term = request.args.get('term')
    core_recs = request.args.get('core_recs')
    dept = request.args.get('dept')
    all_course_info = get_data()
    length = len(all_course_info)
    results = []
    for index in range(length):
        current_course = all_course_info[index]
        match = True
        if year is not None and current_course.year != year:
            match = False
        if term is not None and current_course.season != term:
            match = False
        if core_recs is not None and current_course.core != core_recs:
            match = False
        if dept is not None and current_course.department != dept:
            match = False
        if match:
            results.append(current_course)
    return render_template('filtered_page.html', list=results)


def view_results():
    return render_template('filtered_page.html')


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
