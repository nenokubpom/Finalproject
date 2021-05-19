from flask import Blueprint,render_template,request
import requests
allbands = Blueprint('allbands', __name__)

@allbands.route('/band', methods=['GET','POST'])
def allsearch():
   myurl = 'http://127.0.0.1:5000/girlgroup/band'
   if request.method == 'POST':
      name = str(request.form.get('name'))
      url = '{}/{}'.format(myurl, name)
      data = requests.get(url).json()
      mydata = data
      return render_template('band.html',data = mydata)
   return render_template('band.html')