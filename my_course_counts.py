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

@app.route('/results') # This function needs to have a loop that acquires the right information to be displayed
'''
Basic structure of what goes here:
We might need a loop for each dropdown meun.
new_list=[]
For selection in dropdown:
    take value of selection
    for value in course_data,
        new_list.append all the things at the indices surrounding the thing you selected
If someone selected something from this menu, then, take the value
associated with the thing they checked, and then loop through the course_info list. If the object in the course_info
list matches the thing you clicked on the dropdown, then do basically what we did in the flask lab.
'''

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
