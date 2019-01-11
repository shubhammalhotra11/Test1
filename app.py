from flask import Flask, request
from pymongo import MongoClient
from bson import json_util as json

MONGODB_URI = "mongodb://test:test1234@ds153814.mlab.com:53814/student_db"
client = MongoClient(MONGODB_URI)
db = client.get_database("student_db")
student_record = db.student_record

app = Flask(__name__)

@app.route('/')
def index():
	return "Welcome to Student Records API."

@app.route('/students/', methods=['GET', 'POST'])
def student_list():
	if request.method == 'GET':
		data = list(student_record.find({}))
		return json.dumps(data)

	else:
		try:
			roll_no = int(request.form.get('roll_no'))
			if len(list(student_record.find({'roll_no': roll_no}))):
				return json.dumps({'error': 'This record already exists!'})
			data = dict(request.form)

			student_record.insert_one(data)
			return json.dumps({'result': 'Successfully added'})
		except Exception as e:
			return json.dumps({'error': str(e)})

@app.route('/students/<int:roll_no>', methods = ['GET','PATCH','DELETE'])
def student_detail(roll_no):
	if student_record.count_documents({'roll_no' : roll_no}) is 0:
		return json.dumps({'error' : 'No Record Found'})

	if request.method == 'GET':
		record = student_record.find_one({'roll_no' : roll_no})
		return json.dumps(record)

	elif request.method == 'PATCH':
		record = student_record.find_one({'roll_no' : roll_no})
		record.update(dict(request.form))
		student_record.update_one({'roll_no' : roll_no}, {'$set':record})
		return json.dumps({'result' : 'Successfully updated'})

	else:
		student_record.delete_one({'roll_no' : roll_no})
		return json.dumps({'result' : 'Successfully Deleted'})



if __name__=="__main__":
	app.run(port=8000, debug=True, use_reloader=True)

