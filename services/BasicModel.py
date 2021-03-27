import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api,Resource,request, fields, marshal_with
from werkzeug.security import generate_password_hash,check_password_hash
from flask_jwt import JWT ,jwt_required
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec import marshal_with, doc, use_kwargs

database_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mykeyishere'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(database_dir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
api = Api(app)
migrate = Migrate(app,db)
#jwt = JWT(app, authenticate, identity)

# Creating a disabled persons table
class Disabled(db.Model):
	id = db.Column(db.Integer,primary_key=True)
	
	name = db.Column(db.Text)
	email = db.Column(db.String(64),unique=True,index=True,nullable=False)
	mobile = db.Column(db.Integer)
	password_hash = db.Column(db.String(128))
	exams = db.relationship('Exam',backref='Disabled',lazy='dynamic')
	ratings = db.relationship('Volunteer_Rating',backref='Disabled',lazy='dynamic')
	def __init__(self,name,email,mobile,password):
		self.name =  name
		self.email = email
		self.mobile = mobile
		self.password_hash = generate_password_hash(password)
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)
	def json(self):
		return {"name":self.name,"email":self.email,"mobile":self.mobile}
	def __repr__(self):
		return f"Person who needs Scribe: {self.name}    "

# Creating Volunteer table
class Volunteer(db.Model):
	id = db.Column(db.Integer,primary_key=True)

	name = db.Column(db.Text)
	email = db.Column(db.String(64),unique=True,index=True,nullable=False)
	mobile = db.Column(db.Integer)
	password_hash = db.Column(db.String(128))
	gender = db.Column(db.String(20))
	city_town_village = db.Column(db.String(128))
	state = db.Column(db.String(64))
	pincode = db.Column(db.Integer)
	language_1 = db.Column(db.String(64))
	language_2 = db.Column(db.String(64))
	language_3 = db.Column(db.String(64))
	highest_degree = db.Column(db.String(64))
	vol_status = db.Column(db.String(64),default = "Y")
	examss = db.relationship('Exam',backref='Volunteer',lazy='dynamic')
	ratings = db.relationship('Volunteer_Rating',backref='Volunteer',lazy='dynamic')
	def __init__(self,name,email,mobile,password,gender,city_town_village,state,pincode,language_1,language_2,language_3,highest_degree):
		self.name=name
		self.email = email
		self.mobile = mobile
		self.password_hash = generate_password_hash(password)
		self.gender = gender
		self.city_town_village = city_town_village
		self.state = state
		self.pincode = pincode
		self.language_1 = language_1
		self.language_2 = language_2
		self.language_3 = language_3
		self.highest_degree = highest_degree
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)
	def json(self):
		return {"name":self.name,"email":self.email,"mobile":self.mobile}
	def __repr__(self):
		return f"Volunteer: {self.name}    "

# Creating application master table
class Exam(db.Model):
	id = db.Column(db.Integer,primary_key=True)

	exam_name = db.Column(db.Text)
	exam_date = db.Column(db.String(64))
	exam_start_time = db.Column(db.String(64))
	exam_end_time = db.Column(db.String(64))
	exam_centre_addr = db.Column(db.Text)
	exam_city = db.Column(db.String(64))
	exam_area_pincode = db.Column(db.Integer)
	skills_preference = db.Column(db.Text)
	gender_preference = db.Column(db.String(20))
	language_preference = db.Column(db.String(128))
	disabled_id = db.Column(db.Integer,db.ForeignKey('disabled.id'))
	volunteer_id = db.Column(db.Integer,db.ForeignKey('volunteer.id'))
	def __init__(self,exam_name,exam_date,exam_start_time,exam_end_time,exam_centre_addr,exam_city,exam_area_pincode,skills_preference,gender_preference,language_preference,disabled_id):
		self.exam_name = exam_name	
		self.exam_date = exam_date
		self.exam_start_time = exam_start_time
		self.exam_end_time = exam_end_time
		self.exam_centre_addr = exam_centre_addr
		self.exam_city = exam_city
		self.exam_area_pincode = exam_area_pincode
		self.skills_preference = skills_preference
		self.gender_preference = gender_preference
		self.language_preference = language_preference
		self.disabled_id = disabled_id
	def json(self):
		pass
	def __repr__(self):
		return f"Application ID: {self.id} ------ Disabled person ID: {self.disabled_id} ---- Volunteer ID: {self.volunteer_id}"

##-----------Request/Response Scheema's for swagger
class VounteerRequestSchema(Schema):
    #api_type = fields.String(required=True, description="API type of be my scribe API")
	name =  fields.String(required=True, description="API type of be my scribe API")
	email = fields.String(required=True, description="API type of be my scribe API")
	mobile = fields.String(required=True, description="API type of be my scribe API")
	gender=fields.String(required=True, description="API type of be my scribe API")
	city_town_village=fields.String(required=True, description="API type of be my scribe API")
	state=fields.String(required=True, description="API type of be my scribe API")
	pincode=fields.String(required=True, description="API type of be my scribe API")
	language_1=fields.String(required=True, description="API type of be my scribe API")
	language_2=fields.String(required=True, description="API type of be my scribe API")
	language_3=fields.String(required=True, description="API type of be my scribe API")
	highest_degree=fields.String(required=True, description="API type of be my scribe API")

class VolunteerResponseSchema(Schema):
	name =  fields.Str(default='Success')
	email = fields.Str(default='Success')
	mobile = fields.Str(default='Success')
	gender=fields.Str(default='Success')
	city_town_village=fields.Str(default='Success')
	state=fields.Str(default='Success')
	pincode=fields.Str(default='Success')
	language_1=fields.Str(default='Success')
	language_2=fields.Str(default='Success')
	language_3=fields.Str(default='Success')
	highest_degree=fields.Str(default='Success')

class DisableResponseSchema(Schema):
	name = fields.Str(default='Success')
	email = fields.Str(default='Success')
	mobile = fields.Str(default='Success')
	exams = fields.Str(default='Success')
	ratings = fields.Str(default='Success')
	
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Be My Scribe',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})


# Creating Rating table
class Volunteer_Rating(db.Model):
	id = db.Column(db.Integer,primary_key=True)

	disabled_id = db.Column(db.Integer,db.ForeignKey('disabled.id'))
	volunteer_id = db.Column(db.Integer,db.ForeignKey('volunteer.id'))
	timely_response = db.Column(db.Integer)
	behaviour = db.Column(db.Integer)
	feedback = db.Column(db.Text)
	def __init__(self,disabled_id,volunteer_id,timely_response,behaviour,feedback):
		self.disabled_id = disabled_id
		self.volunteer_id = volunteer_id
		self.timely_response = timely_response
		self.behaviour = behaviour
		self.feedback = feedback
	def json(self):
		pass
	def __repr__(self):
		return f"Feedback ID: {self.id} ------ Disabled person ID: {self.disabled_id} ---- Volunteer ID: {self.volunteer_id}"



#disabledregister
class DisabledRegister(Resource):
	def post(self):
		data = request.get_json()
		name = data["name"]
		email = data["email"]
		mobile = data["mobile"]
		disabled_user = Disabled(name=name,email=email,mobile=mobile)
		db.session.add(disabled_user)
		db.session.commit()
		return disabled_user.json()

#volunteerregister
class VolunteerRegister(MethodResource, Resource):
	@doc(description='Add new volunteer API.', tags=['Vounteer'])
	@use_kwargs(VounteerRequestSchema, location=('json'))
	@marshal_with(VolunteerResponseSchema)  # marshalling with marshmallow library
	def post(self):
		data = request.get_json()
		name = data["name"]
		email = data["email"]
		mobile = data["mobile"]
		gender=data["gender"]
		city_town_village=data["city_town_village"]
		state=data["state"]
		pincode=data["pincode"]
		language_1=data["language_1"]
		language_2=data["language_2"]
		language_3=data["language_3"]
		highest_degree=data["highest_degree"]
#		vol_status=data["vol_status"]
		volunteer_user = Volunteer(name=name,email=email,mobile=mobile,gender=gender,city_town_village=city_town_village,state=state,pincode=pincode,language_1=language_1,language_2=language_2,language_3=language_3,highest_degree=highest_degree)
		db.session.add(volunteer_user)
		db.session.commit()
		return volunteer_user.json()

# Fetch user
class DisabledResource(MethodResource, Resource):
	@doc(description='Get disabled info API.', tags=['Disable'])
	@marshal_with(DisableResponseSchema)  # marshalling with marshmallow library
	def get(self,email):
		disabled_user = Disabled.query.filter_by(email=email).first()
		if disabled_user:
			return disabled_user.json(), 200
		else:
			return {'email':'not found'}, 404



api.add_resource(DisabledResource,'/disabled/<string:email>')
api.add_resource(DisabledRegister,'/disabledRegister')
api.add_resource(VolunteerRegister,'/volunteerRegister')

# Add newly created api to swagger docs
docs = FlaskApiSpec(app)
docs.register(DisabledResource)
docs.register(VolunteerRegister)

# Implementing JWT 
def authenticate(email, password):
	if bool(Disabled.query.filter_by(email = email).first()):
		user = Volunteer.query.filter_by(email = email).first()
	else:
		user = Disabled.query.filter_by(email = email).first()
	if user and user.check_password(password):
		return user

# identity function here


app.run(port=5000,debug=True)