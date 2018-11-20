from flask import Flask,render_template
from flask import Flask, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, BooleanField, StringField, IntegerField, validators
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)
app.config['SECRET_KEY']='HELLO WORLD'
app.config['FLASK_ADMIN_SWATCH'] = 'Cyborg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONs'] = False
admin = Admin(app, name='BUS', template_mode='bootstrap3')
db=SQLAlchemy(app)


class User(db.Model):
	_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name=db.Column(db.String(20),nullable=False)
	email = db.Column(db.String(120), nullable=False)
	phone = db.Column(db.Integer(),nullable=False)
	friday_go=db.Column(db.Boolean())
	sat_go=db.Column(db.Boolean())
	sat_ret=db.Column(db.Boolean())
	sun_ret=db.Column(db.Boolean())
	faculty=db.Column(db.Boolean())

	def __init__(self, name, email, phone, friday_go, sat_go, sat_ret, sun_ret,faculty):
		self.name = name
		self.email = email
		self.phone = phone
		self.friday_go = friday_go
		self.sat_go = sat_go
		self.sat_ret = sat_ret
		self.sun_ret = sun_ret
		self.faculty=faculty


	def __repr__(self):
		return f"User('{self.user_id}', '{self.name}', '{self.email}', '{self.phone}', '{self.friday_go}', '{self.sat_go}', '{self.sat_ret}', '{self.sun_ret}', '{self.faculty}')"

admin.add_view(ModelView(User, db.session))

class RegistrationForm(Form):
	name= StringField('Name',[validators.DataRequired()])
	email = StringField('Email Address', [validators.Length(min=6, max=35),validators.Email(message="Invalid Email")])
	phone = IntegerField('Phone Number', [validators.NumberRange(min=1111111111,max=9999999999),validators.DataRequired()])
	friday_go = BooleanField('Friday Going')
	sat_go = BooleanField('Saturday Going')
	sat_ret = BooleanField('Saturday Return ')
	sun_ret = BooleanField('Sunday Coming')
	faculty = BooleanField('Check for Faculty')


db.create_all()


@app.route('/')
@app.route("/home")
def home():
	return render_template('home.html')
@app.route("/contact")
def contact():
	return render_template('contact.html')





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.name.data, form.email.data,
                    form.phone.data,form.friday_go.data,form.sat_go.data,form.sat_ret.data,form.sun_ret.data,form.faculty.data)
        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template('register.html', form=form)


@app.route("/details")
def details():
	return render_template('details.html')

@app.route("/admin1",methods=['GET','POST'])
def admin1():
	error = None
	if request.method == 'POST':
		if request.form['username'] == 'admin' or request.form['password'] == 'admin':
			return redirect('/admin/user')
		
	return render_template('admin.html')



#TESTTTTTT

if __name__ == '__main__':
   app.run(debug = True)



