import requests
from time import sleep
# r = requests.get('https://loadbalancer:8081/todo/api/v1.0/tasks', verify=False, auth=('przemek','python'))
# r = requests.put('http://loadbalancer/todo/api/v1.0/tasks/2', verify=False, data = {"done":True}, auth=('przemek','python'))
# r = requests.get('http://loadbalancer/todo/api/v1.0/tasks', verify=False, auth=('przemek','python'))

# r = requests.get('http://loadbalancer/rsosnapchat/api/v1.0/addUser', verify=False)

# r = requests.post('http://loadbalancer/rsosnapchat/api/v1.0/addUser', verify=False, json={'name': 'nowyUser', 'login': 'nowyUser2', 'password': 'password123'})
sleep(5)
r = requests.post('https://loadbalancer_2', verify=False)
print(r)
print(r.content)