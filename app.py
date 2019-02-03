from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

#Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Init db
db = SQLAlchemy(app)

#Intit ma
ma = Marshmallow(app)

#Product
class Entry(db.Model):
	p_id = db.Column(db.Integer, primary_key=True)
	ping = db.Column(db.Float)
	download = db.Column(db.Float)
	upload = db.Column(db.Float)
	date = db.Column(db.String)

	def __init__(self, ping, download, upload, date):
		self.ping = ping
		self.download = download
		self.upload = upload
		self.date = date

#Entry Schema
class EntrySchema(ma.Schema):
	class Meta:
		fields = ('p_id', 'ping', 'download', 'upload', 'date')

#Init Schema
entry_schema = EntrySchema(strict=True)
entries_schema = EntrySchema(many=True, strict=True)

#Create a Entry
@app.route('/api/vi/entry', methods=['POST'])
def add_entry():
	ping = request.json['ping']
	download = request.json['download']
	upload = request.json['upload']
	date = request.json['date']

	new_entry = Entry(ping, download, upload, date)

	db.session.add(new_entry)
	db.session.commit()

	return entry_schema.jsonify(new_entry)

#Get All Entries
@app.route('/api/vi/entry', methods=['GET'])
def get_entries():
	all_entries = Entry.query.all()
	result = entries_schema.dump(all_entries)
	return jsonify(result.data)

#Get A Entry
@app.route('/api/vi/entry/<p_id>', methods=['GET'])
def get_entry(p_id):
	entry = Entry.query.get(p_id)
	return entry_schema.jsonify(entry)

#Delete A Entry
@app.route('/api/vi/entry/<p_id>', methods=['DELETE'])
def delete_entry(p_id):
	entry = Entry.query.get(p_id)
	db.session.delete(entry)
	db.session.commit()
	return entry_schema.jsonify(entry)

#Run Server
if __name__ == '__main__':
	app.run(debug=True)