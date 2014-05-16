#!flask/bin/python
from flask import Flask,jsonify,abort,request, url_for

app = Flask(__name__)

tasks = [
    {
        'id':1,
        'title': u'PIR no 151',
        'description': u'fixed it in record time',
        'time': u'1250',
        'done': True
    },
    {
        'id':2,
        'title': u'PIR no 152',
        'description': u'fixed it in record time',
        'time': u'1450',
        'done': True
    }
]
'''
change the path to whatever - placeholder path used from tutorial on
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
'''

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task',task_id = task['id'], _external= True)
        else:
            new_task[field] = task[field]
    return new_task

@app.route('/nilas/api/v1.0/tasks',methods =['GET'])
def get_tasks():
    return jsonify({'tasks':map(make_public_task,tasks)})


@app.route('/nilas/api/v1.0/tasks/<int:task_id>',methods =['GET'])
def get_task(task_id):
    task = filter(lambda t:t['id']==task_id,tasks)
    if(len(task))==0:
        return jsonify({'error':'Not Found'}),404
    return jsonify({'task':task[0]})


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error':'Not Found'}),404


@app.route('/nilas/api/v1.0/tasks',methods =['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        return jsonify({'error':'Not Found'}),404
    task ={
        'id': tasks[-1]['id'] + 1 ,
        'title': request.json['title'],
        'description': request.json.get('description',""),
        'time': request.json.get('time',""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task':task}),201

@app.route('/nilas/api/v1.0/tasks/<int:task_id>',methods = ['PUT'])
def update_task(task_id):
    task=filter(lambda t:t['id'] == task_id,tasks)
    if(len(task)==0):
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title'])!=unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description'])!=unicode:
        abort(400)
    if 'time' in request.json and type(request.json['time'])!=unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done'])is not bool:
        abort(400)
    task[0]['title']=request.json.get('title',task[0]['title'])
    task[0]['description']=request.json.get('description',task[0]['description'])
    task[0]['time']=request.json.get('time',task[0]['time'])
    task[0]['done']=request.json.get('done',task[0]['done'])
    return jsonify({'task':task[0]})

@app.route('/nilas/api/v1.0/tasks/<int:task_id>',methods = ['DELETE'])
def delete_task(task_id):
    task=filter(lambda t:t['id']==task_id,tasks)
    if len(task) ==0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({'result':True})


    
    
if __name__ == '__main__':
    app.run(debug=True)
    
    