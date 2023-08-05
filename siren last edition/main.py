import select

from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,logout_user,login_manager,LoginManager
from flask_login import login_required,current_user
from flask_mail import Mail,smtplib
import json





# with open('config.json','r') as c:
#     params =json.load(c)["params"]








# MY db connection
local_server= True
app = Flask(__name__)
app.secret_key='none'

#app.config.update(
#     MAIL_SERVER='smtp.gmail.com',
#     MAIL_PORT='587',
#     MAIL_USER_SSL=True,
#     MAIL_USERNAME=params['gmail-user'],
#     MAIL_PASSWORD= params['gmail-password']

# )
# mail=Mail(app)
# this is for getting unique user access
login_manager=LoginManager(app)
login_manager.login_view='login'
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))




#data base connection ------------------------------------------------------------------------------------------------

# app.config['SQLALCHEMY_DATABASE_URL']='mysql://username:password@localhost/databas_table_name'
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:@localhost/siren'
db=SQLAlchemy(app)



# here we will create db models that is tables
#table class init ----------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------
class Test(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100))

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(50))
    email=db.Column(db.String(50),unique=True)
    password=db.Column(db.String(1000))

class Driver(db.Model):
    did=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50))
    gender=db.Column(db.String(20))
    aadhar=db.Column(db.String(20))
    number=db.Column(db.String(20))

class Ambulance(db.Model):
    aid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    vtype=db.Column(db.String(50))
    vnumber=db.Column(db.String(50))

class Manage(db.Model):
    mid=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(50))
    name=db.Column(db.String(50))
    vnumber=db.Column(db.String(50))


class Book(db.Model):
    bid=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    pemail=db.Column(db.String(50),unique=True)
    gender=db.Column(db.String(50))
    symptoms=db.Column(db.String(50))
    number=db.Column(db.String(20))
    vtype=db.Column(db.String(50))
    email=db.Column(db.String(50))
    state=db.Column(db.String(20))
    city=db.Column(db.String(20))
    latitude=db.Column(db.String(50))
    longitude=db.Column(db.String(50))






#rendering page or routing section --------------------------------------------------------------------------------------------

@app.route('/')
def index(): 
    return render_template('sirenbase.html')



@app.route('/book',methods=['POST','GET'])
def book():
    
    drive=db.engine.execute(f"SELECT * FROM `driver`")
    amb=db.engine.execute(f"SELECT * FROM `ambulance`")
    use=db.engine.execute(f"SELECT * FROM `user`")
    if request.method=="POST":
             name=request.form.get('name')
             pemail=request.form.get('pemail')
             gender=request.form.get('gender')
             symptoms=request.form.get('symptoms')
             number=request.form.get('number')
             vtype=request.form.get('vtype')
             email=request.form.get('email')
             latitude=request.form.get('latitude')
             longitude=request.form.get('longitude')

            
             query=db.engine.execute(f" INSERT INTO `book` (`name`,`pemail`,`number`,`vtype`,`email`,`latitude`,`longitude`) VALUES ('{name}','{pemail}','{number}','{vtype}','{email}','{latitude}','{longitude}')")
             flash("Driver added","success")
            
             return redirect('/')
                                  


    return render_template('book.html',drive=drive,amb=amb,use=use)

@app.route('/booking',methods=['POST','GET'])
@login_required
def booking():
    em=current_user.email
    query=db.engine.execute(f"SELECT * FROM `book` WHERE email='{em}'")
    return render_template('bookinglist.html',query=query)

@app.route("/delete3/<string:bid>",methods=['POST','GET'])
@login_required
def delete3(bid):
    db.engine.execute(f"DELETE FROM `book` WHERE `book`.`bid`={bid}")
    flash("Driver removed","danger")
    return redirect('/booking')














#home page -----------------------------------------------------------------------------------------------------------

@app.route('/maindash',methods=['POST','GET'])
@login_required
def maindash():
    em=current_user.email
    query=db.engine.execute(f"SELECT * FROM `manage` WHERE email='{em}'")
    man=db.engine.execute(f"SELECT * FROM `book`")
    return render_template('maindash.html',query=query,man=man)

@app.route('/manage',methods=['POST','GET'])
@login_required
def manage():
    em=current_user.email
    drive=db.engine.execute(f"SELECT * FROM `driver` WHERE email='{em}'")
    amb=db.engine.execute(f"SELECT * FROM `ambulance`WHERE email='{em}'")
    man=db.engine.execute(f"SELECT * FROM `book` WHERE email='{em}'")
    if request.method=="POST":
             name=request.form.get('name')
             email=request.form.get('email')
             vnumber=request.form.get('vnumber')
             pname=request.form.get('pname')
             query=db.engine.execute(f" INSERT INTO `manage` (`email`,`name`,`vnumber`,`pname`) VALUES ('{email}','{name}','{vnumber}','{pname}')")
             flash("Driver added","success")
             return redirect('/maindash')
            
    
    return render_template('manage.html',drive=drive,amb=amb,man=man)

@app.route("/delete2/<string:mid>",methods=['POST','GET'])
@login_required
def delete2(mid):
    db.engine.execute(f"DELETE FROM `manage` WHERE `manage`.`mid`={mid}")
    
    return redirect('/maindash')










#driver==================================================================================================
@app.route('/driver',methods=['POST','GET'])
@login_required
def driver():
    em=current_user.email
    query=db.engine.execute(f"SELECT * FROM `driver` WHERE email='{em}'")
    return render_template('driver.html',query=query)

@app.route('/adddriver',methods=['POST','GET'])
def adddriver():
    if request.method=="POST":
             email=request.form.get('email')
             name=request.form.get('name')
             gender=request.form.get('gender')
             aadhar=request.form.get('aadhar')
             number=request.form.get('number')
             query=db.engine.execute(f" INSERT INTO `driver` (`email`,`name`,`gender`,`aadhar`,`number`) VALUES ('{email}','{name}','{gender}','{aadhar}','{number}')")
             flash("Driver added","success")
             return redirect('/driver')
            
    
    return render_template('adddriver.html')


@app.route("/edit/<string:did>",methods=['POST','GET'])
@login_required
def edit(did):
    posts=Driver.query.filter_by(did=did).first()
    if request.method=="POST":
        email=request.form.get('email')
        name=request.form.get('name')
        gender=request.form.get('gender')
        aadhar=request.form.get('aadhar')
       
        number=request.form.get('number')
        db.engine.execute(f"UPDATE `driver` SET `email` = '{email}', `name` = '{name}', `gender` = '{gender}',`aadhar` = '{aadhar}', `number` = '{number}' WHERE `driver`.`did` = {did}")
        flash("Slot is Updates","success")
        return redirect('/driver')
    
    return render_template('edit.html',posts=posts)


@app.route("/delete/<string:did>",methods=['POST','GET'])
@login_required
def delete(did):
    db.engine.execute(f"DELETE FROM `driver` WHERE `driver`.`did`={did}")
    flash("Driver removed","danger")
    return redirect('/driver')




#ambulance========================================================================================================
@app.route('/ambulance',methods=['POST','GET'])
@login_required
def ambulance():
    em=current_user.email
    query=db.engine.execute(f"SELECT * FROM `ambulance` WHERE email='{em}'")
    return render_template('ambulance.html',query=query)

@app.route('/addamb',methods=['POST','GET'])
def addamb():
    if request.method=="POST":
             email=request.form.get('email')
             vtype=request.form.get('vtype')
             vnumber=request.form.get('vnumber')
             query=db.engine.execute(f" INSERT INTO `ambulance` (`email`,`vtype`,`vnumber`) VALUES ('{email}','{vtype}','{vnumber}')")
             return redirect('/ambulance')
    return render_template('addamb.html')

@app.route("/editamb/<string:aid>",methods=['POST','GET'])
@login_required
def editamb(aid):
    posts=Ambulance.query.filter_by(aid=aid).first()
    if request.method=="POST":
        email=request.form.get('email')
        vtype=request.form.get('vtype')
        vnumber=request.form.get('vnumber')
       
        db.engine.execute(f"UPDATE `ambulance` SET `email` = '{email}', `vtype` = '{vtype}', `vnumber` = '{vnumber}'  WHERE `ambulance`.`aid` = {aid}")
        flash("Slot is Updates","success")
        return redirect('/ambulance')
    
    return render_template('editamb.html',posts=posts)

@app.route("/deleteamb/<string:aid>",methods=['POST','GET'])
@login_required
def deleteamb(aid):
    db.engine.execute(f"DELETE FROM `ambulance` WHERE `ambulance`.`aid`={aid}")
    flash("Driver removed","danger")
    return redirect('/ambulance')
            






    
















@app.route('/signup',methods=['POST','GET'])
def signup():

    if request.method == "POST":
        username=request.form.get('username')
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("Email Already Exist","warning")
            return render_template('/signup.html')
        encpassword=generate_password_hash(password)

        new_user=db.engine.execute(f"INSERT INTO `user` (`username`,`email`,`password`) VALUES ('{username}','{email}','{encpassword}')")

        # this is method 2 to save data in db
        # newuser=User(username=username,email=email,password=encpassword)
        # db.session.add(newuser)
        # db.session.commit()
        flash("Signup Succes Please Login now","success")
        return render_template('login.html')

    return render_template('signup.html')




    


















@app.route('/login',methods=['POST','GET'])
def login():
    if request.method == "POST":
        email=request.form.get('email')
        password=request.form.get('password')
        user=User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password,password):
            login_user(user)
            flash("Login Success","primary")
            return render_template('maindash.html')
        else:
            flash("invalid credentials","danger")
            return render_template('login.html')    

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logout SuccessFul","warning")
    return redirect(url_for('login'))





@app.route('/test')
def test():
    try:
        Test.query.all()
        return 'My database is Connected'
    except:
        return 'My db is not Connected'


app.run(debug=True)    