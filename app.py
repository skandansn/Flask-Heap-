from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField,PasswordField,BooleanField
from wtforms.validators import InputRequired,Email,Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

import Heap as h
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY']="sec"
Bootstrap(app)
heap = h.MaxHeap(2**10 - 1)
flag = 0


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    city = db.Column(db.String(25))


@login_manager.user_loader
def load_user(user_id):
    global flag
    flag=0
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    city=StringField('city', validators=[InputRequired(), Length(min=3, max=25)])





class Lists(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.String(200),nullable=False)
    priority = db.Column(db.Integer,nullable=False)
    city = db.Column(db.String(25),nullable=False)


    def __repr__(self):
        return '<Element %r>' %self.id

@app.route('/home', methods=['POST','GET'])
@login_required
def insertHome():     
    delv = heap.extractMax()
    while(delv!=None):
        delv=heap.extractMax()
    list = Lists.query.order_by(Lists.id).all()   
    values=[]
    neededlist=[]
    priorities=[]
    for i in list:
        if(i.city==current_user.city):
            neededlist.append(i)
            values.append(i.content)
            priorities.append(i.priority)
    if(values!=None and heap.Heap==None):
        for i in list:
            if(i.city==current_user.city):
                neededlist.append(i)
                values.append(i.content)
                priorities.append(i.priority)
                heap.insert(i.priority,i.content)

    if request.method == 'POST':
        sent_elem = request.form['content']
        v,p=0,0
        try:
            v,p=map(str,sent_elem.split())
        except:
            return "Please enter space seperated values while inserting a value"
        heap.insert(int(p),v)
        new_val =Lists(content=v,priority=p,city=current_user.city)
        try:
            db.session.add(new_val)
            db.session.commit()
            return redirect('/home')
        except:
            return 'Error'
    else:
      
        list = Lists.query.order_by(Lists.id).all()
        values=[]
        neededlist=[]
        priorities=[]
        global flag
        for i in list:
            if(i.city==current_user.city):
                neededlist.append(i)
                values.append(i.content)
                priorities.append(i.priority)
                if flag == 0:
                    heap.insert(i.priority,i.content)
        flag = 1
        print("Values are",values,"Priorities are",priorities)
        return render_template('home.html',name=current_user.username ,city=current_user.city,items = neededlist,delv=request.args.get('delv'))

@app.route('/delete')
def delete():
    insertHome()

    delv = heap.extractMax()
    if(delv is not None):
        obj = Lists.query.filter_by(priority = delv).first()
        if(obj.city==current_user.city):
            item_to_delete = Lists.query.get_or_404(obj.id)
            try:    
                db.session.delete(item_to_delete)
                db.session.commit()
                return redirect(url_for('.insertHome', delv=str(obj.content)+" (age "+str(obj.priority)+") just got vaccinated."))

            except:
                return 'Error Deleting'
        else:
            while(delv!=None):
                delv=heap.extractMax()
                if(delv==None):
                    return "Error Deleting"
                obj = Lists.query.filter_by(priority = delv).first()
                if(obj.city==current_user.city):
                    item_to_delete = Lists.query.get_or_404(obj.id)
                    try:    
                        db.session.delete(item_to_delete)
                        db.session.commit()
                        return redirect(url_for('.insertHome', delv=str(obj.content)+" (age "+str(obj.priority)+") just got vaccinated."))

                    except:
                        return 'Error Deleting'

    else:
        return "Insert elements first to delete"
    return redirect('/home')

        
        

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        user=User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                global flag
                flag=0
                return redirect(url_for('insertHome'))
        return '<h1>Invalid uname or password</h1>'
            
    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        new_user=User(username=form.username.data, email=form.email.data, password=hashed_password,city=form.city.data)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html',form=form)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    delv = heap.extractMax()
    while(delv!=None):
        delv=heap.extractMax()


    return redirect(url_for('index'))


if __name__ == '__main__':

    app.run(debug=True)