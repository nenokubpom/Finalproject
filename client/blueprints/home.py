from flask import Blueprint,render_template,request
home = Blueprint('home', __name__)
import requests

@home.route('/home', methods=['GET','POST'])
def index():
   myurl = 'http://127.0.0.1:5000/girlgroup/'
   if request.method == 'POST':
      name = str(request.form.get('name'))
      url = '{}/{}'.format(myurl, name)
      data = requests.get(url).json()
      mydata = data
      return render_template('name.html',data = mydata)
   return render_template('name.html')