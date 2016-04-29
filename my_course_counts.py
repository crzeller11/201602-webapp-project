from os import chdir
from os.path import dirname, realpath

from flask import Flask, render_template, send_from_directory, request

app = Flask(__name__)

# FIXME write your app below

class Course_Info:
    def __init__(self, year, term, dept, course_num, section, title, units, professor, schedule, core_recs,
                 total_seats, enrolled, reserved, reserved_open, waitlisted):
        self.year = year
        self.term = term
        self.dept = dept
        self.course_num = course_num
        self.section = section
        self.title = title
        self.units = units
        self.professor = professor
        self.schedule = schedule
        self.core_recs = core_recs
        self.total_seats = total_seats
        self.enrolled = enrolled
        self.reserved = reserved
        self.reserved_open = reserved_open
        self.waitlisted = waitlisted

def get_data():
    course_data = []
    with open('counts.tsv') as file:
        for line in file.read().splitlines():
            year, term, dept, course_num, section, title, units, professor, schedule, core_recs, total_seats, \
            enrolled, reserved, reserved_open, waitlisted = line.split('\t')
            professor = professor.replace(';', '; ')
            core_recs = core_recs.replace(';', '; ')
            course_data.append(Course_Info(year, term, dept, course_num, section, title, units, professor,
            schedule, core_recs, total_seats, enrolled, reserved, reserved_open, waitlisted))
    return course_data

def get_prof_list():
    list_of_prof = []
    course_data = get_data()
    for instance in course_data:
        if instance.professor not in list_of_prof:
            list_of_prof.append(instance.professor)
    return sorted(list_of_prof)

# check the course_info class and just see if that's the right thing to do and then check the get_data function. I don't
# think the list course_data needs to be sorted like in did in the flask lab, because we aren't searching for anything in
# particular like we were before.

'''
Things we need:
HTML file that displays results (filtered_page)
Design, what should entire website looks like, what should CSS look like? What should whole design look like
'''

@app.route('/')
def view_root():
    list_of_prof = get_prof_list()
    return render_template('base.html', list_of_prof=list_of_prof)

@app.route('/results')
def view_course_info():
    year = request.args.get('year')
    term = request.args.get('term')
    core_recs = request.args.get('core_recs')
    dept = request.args.get('dept')
    professor = request.args.get('professor')
    all_course_info = get_data()
    refined_year = []
    refined_term = []
    refined_core_recs = []
    refined_dept = []
    results = []
    if year == "Please Select a Year":
        refined_year = all_course_info
    if year is not None:
        for instance in all_course_info:
            if instance.year == year:
                refined_year.append(instance)
    if term == "Please Select a Term":
        refined_term = refined_year
    if term is not None:
        for instance in refined_year:
            if instance.term == term:
                refined_term.append(instance)
    if core_recs == "Please Select Core":
        refined_core_recs = refined_term
    # Add the instance to refined_core_recs list only if the core_recs of the instance is found in the list of core_recs
    if core_recs is not None:
        for instance in refined_term:
            if instance.core_recs.find(core_recs) != -1:
                refined_core_recs.append(instance)
    if dept == "Please Select a Department":
        refined_dept = refined_core_recs
    if dept is not None:
        for instance in refined_core_recs:
            if instance.dept == dept:
                refined_dept.append(instance)
    if professor == "Please Select a Professor":
        results = refined_dept
    # Add the instance to results list only if the professor name of the instance is found in the list of professors
    if professor is not None:
        for instance in refined_dept:
            if instance.professor.find(professor) != -1:
                results.append(instance)
    return render_template('filtered_page.html', results=results)

'''
ADDITIONS:
- Search through course descriptions, maybe redirect to a separate page
- Add a search bar that searches like Justin's app does. Conducts a much broader search
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