from flask import Blueprint,render_template,request
fromyear = Blueprint('fromyear', __name__)
import requests

@fromyear.route('/year', methods=['GET','POST'])
def index():
   myurl = 'http://127.0.0.1:5000/girlgroup/searchyear/'
   if request.method == 'POST':
      year = str(request.form.get('year'))
      url = '{}/{}'.format(myurl, year)
      data = requests.get(url).json()
      mydata = data
      return render_template('year.html',data = mydata)
   return render_template('year.html')