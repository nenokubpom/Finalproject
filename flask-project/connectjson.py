import json
open_json = open('Girlgroup.json', 'r') 
read_json = open_json.read()
girlgroup_data = json.loads(read_json)


open_jsonuser = open('request.json', 'r') 
read_jsonuser = open_jsonuser.read()
user = json.loads(read_jsonuser)


def show():
    return girlgroup_data

def showuser():
    return user

def add(request):
    open_json1 = open('request.json', 'w')
    user.append(request)
    json.dump(user,open_json1)
    return 200

def updatedata(memberdata):
    open_json = open('Girlgroup.json', 'w')
    for count,i in enumerate(girlgroup_data):
        if i['Name'].upper() == memberdata['Name'].upper():
            memberdata['Name'] = i['Name']
            girlgroup_data[count].update(memberdata)
            json.dump(girlgroup_data,open_json)
            return 200
        else:
            girlgroup_data.append(memberdata)
            json.dump(girlgroup_data,open_json)
            return 200

    return 400 


def deletereq(namedelete):
    open_json = open('request.json', 'w')
    for i in user:
        if i['name'].upper() == namedelete.upper():
            user.remove(i)
            json.dump(user,open_json)
            return 200
    return 400 

