from flask import Flask,jsonify,abort,request

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

@app.route('/nilas/api/v1.0/tasks',methods =['GET'])
def get_tasks():
    return jsonify({'tasks':tasks})


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

if __name__ == '__main__':
    app.run(debug=True)
    
    