from flask import Flask, jsonify, abort, make_response
from flask.ext.restful import Api, Resource, reqparse, fields, marshal
from flask.ext.httpauth import HTTPBasicAuth

app = Flask(__name__, static_url_path="")
api = Api(app)
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'przemek':
        return 'python'
    return None


@auth.error_handler
def unauthorized():
    # return 403 instead of 401 to prevent browsers from displaying the default
    # auth dialog
    return make_response(jsonify({'message': 'Unauthorized access'}), 403)


tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]

task_fields = {
    'title': fields.String,
    'description': fields.String,
    'done': fields.Boolean,
    'uri': fields.Url('task')
}

profiles = [
    {
        'id': 1,
        'name': 'Przemek',
        'login': 'przlada',
        'password': 'python',
        'friends': [1,2,3,4],
        'photos': [1,2,3,4,5,6]
    }
]

class User(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('login', type=str, required=True, help='You must provide login', location='json')
        self.reqparse.add_argument('password', type=str, required=True, help='You must provide password', location='json')
        self.reqparse.add_argument('name', type=str, required=True, help='You must provide user name', location='json')
        super(User, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        profile = [profile for profile in profiles if profile['login'] == args['login']]
        if len(profile) == 0:
            profile = {
                'id': profiles[-1]['id'] + 1,
                'name': args['name'],
                'login': args['login'],
                'password': args['password'],
                'friends': [],
                'photos': []
            }
            profiles.append(profile)
            return {'profile': profile}, 201
        else:
            abort(404)

    def get(self):
        return profiles, 200

class Profile(Resource):
    decorators = [auth.login_required]
    def get(self):
        profile = [profile for profile in profiles if profile['login'] == auth.username()]
        if len(task) == 0:
            abort(404)
        return {'profile': profile}

class TaskListAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, required=True, help='No task title provided', location='json')
        self.reqparse.add_argument('description', type=str, default="",
                                   location='json')
        super(TaskListAPI, self).__init__()

    def get(self):
        return {'tasks': [marshal(task, task_fields) for task in tasks]}

    def post(self):
        args = self.reqparse.parse_args()
        task = {
            'id': tasks[-1]['id'] + 1,
            'title': args['title'],
            'description': args['description'],
            'done': False
        }
        tasks.append(task)
        return {'task': marshal(task, task_fields)}, 201


class TaskAPI(Resource):
    decorators = [auth.login_required]

    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('title', type=str, location='json')
        self.reqparse.add_argument('description', type=str, location='json')
        self.reqparse.add_argument('done', type=bool, location='json')
        super(TaskAPI, self).__init__()

    def get(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        return {'task': marshal(task[0], task_fields)}

    def put(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        task = task[0]
        args = self.reqparse.parse_args()
        for k, v in args.items():
            if v is not None:
                task[k] = v
        return {'task': marshal(task, task_fields)}

    def delete(self, id):
        task = [task for task in tasks if task['id'] == id]
        if len(task) == 0:
            abort(404)
        tasks.remove(task[0])
        return {'result': True}



api.add_resource(TaskListAPI, '/todo/api/v1.0/tasks', endpoint='tasks')
api.add_resource(TaskAPI, '/todo/api/v1.0/tasks/<int:id>', endpoint='task')
api.add_resource(User, '/rsosnapchat/api/v1.0/addUser', endpoint='addUser')
api.add_resource(Profile, '/rsosnapchat/api/v1.0/getProfile', endpoint='getProfile')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')