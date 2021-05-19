from flask import Blueprint,render_template

all = Blueprint('all', __name__)

@all.route('/all')
def allsearch():
   return render_template('showdata.html')