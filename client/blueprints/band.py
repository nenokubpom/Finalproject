from flask import Blueprint,render_template

band = Blueprint('band', __name__)

@band.route('/band')
def bandsearch():
   return render_template('showdata.html')