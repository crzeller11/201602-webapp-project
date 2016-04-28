import csv
from os import chdir
from os.path import dirname, realpath

from flask import Flask, render_template, send_from_directory, request

TSV_FILE = 'counts.tsv'

app = Flask(__name__)


class Course_Info:
    def __init__(self, row):
        for k in row.keys():
            setattr(self, k, row[k])


def get_data():
    course_data = []
    with open(TSV_FILE, 'r') as tsvfile:
        for row in csv.DictReader(tsvfile, delimiter='\t'):

            row['instructors'] = row['instructors'].replace(';', ', ')

            # Rename some keys
            # PHASE THESE OUT
            row['course_num'] = row.pop('number')
            row['professor'] = row.pop('instructors')
            row['schedule'] = row.pop('meetings')
            row['core_recs'] = row.pop('core')
            row['total_seats'] = row.pop('seats')

            course_data.append(Course_Info(row))
    return course_data


def get_prof_list():
    list_of_prof = []
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
    season = request.args.get('term')
    core_recs = request.args.get('core_recs')
    department = request.args.get('dept')
    professor = request.args.get('professor')

    results = course_data

    if year != "Please Select a Year":
        results = [course for course in results if course.year == year]

    if season != "Please Select a Term":
        results = [course for course in results if course.season == season]

    if core_recs != "Please Select Core":
        results = [course for course in results if core_recs in course.core_recs]

    if department != "Please Select a Department":
        results = [course for course in results if course.department == department]

    if professor != "Please Select a Professor":
        results = [course for course in results if professor in course.professor]

    return render_template('filtered_page.html', results=results)


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
    course_data = get_data()
    app.run(debug=True)
