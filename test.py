from flask import Flask ,render_template,request, session ,redirect # flask is a micro frame work for web development
from flask_sqlalchemy import SQLAlchemy   #sqlalchemy is used for database
from datetime import datetime



app = Flask(__name__)
app.secret_key = 'hello-world'                                                    #this is the syntax for making the flask framework bcoz flask treated as app
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:@127.0.0.1/codingthunder"   #this is for making the connection with database
db = SQLAlchemy(app)                                                              #this is for making conection , with database

#---------------------------------------------------------------------------------------------------------------------------



class Contacts(db.Model):                                 # this class is used for intreacting with database,
    sno = db.Column(db.Integer, primary_key=True)         # or LHS me vo variable hai jo database m bnae the .
    name = db.Column(db.String(80),  nullable=False)      # class name vo ayega jo hmne database bnaya hai, or baki sara syntax hai usme koi change nhi krna .
    phone_num = db.Column(db.String(15),  nullable=False)
    msg = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12), nullable=False)
    email = db.Column(db.String(120),  nullable=False)

class Posts(db.Model):                                # ye class post k lie bnai hai ,sara same hai database se intract krane k lie
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80),  nullable=False)
    slug = db.Column(db.String(21),  nullable=False)
    content = db.Column(db.String(120),  nullable=False)
    date = db.Column(db.String(12),  nullable=False)
    img_file = db.Column(db.String(25), nullable=False)

#-----------------------------------------------------------------------------------------------------------------------------

@app.route("/home")                                       # ye important cheex hai , sara syntax hai change bs bracket k bich vala krna hai , or vha jo ayega jisko hmne route krna hai website p.
def home():
     posts = Posts.query.filter_by().all()[0:6]           # home hmara function hai jsik ander m call krwaenge cheeze.
     return render_template('index.html',posts= posts)    # render_template() ek function hai to hmko isko import krwanahota hai fir,hm isme apni html page ka name dete hai.


#----------------------------------------------------------------------------------------------------------------------------


@app.route("/about")
def about():

    return render_template('about.html')


#---------------------------------------------------------------------------------------------------------------------------


@app.route("/dashboard", methods= ['GET','POST'])
def login():

    if ('user' in session and session['user'] == "harsh"):
        posts = Posts.query.filter_by().all()
        return render_template('dashboard.html')

    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('pass')
        if username == "harsh" and password == "12345678":
            session['user'] = username
            return render_template('dashboard.html')

    return render_template('login.html')

#-----------------------------------------------------------------------------------------------------------------------------


@app.route("/post/<string:post_slug>", methods = ['GET'])    # YE VALA BHI BOHT IMPORTANT HAI(is syntax se hm koi bhi data fetch kra skte hai.)
def post_route(post_slug):                 # jo string upr pass krwai hai vohi niche function m  call krwaenge .
    post = Posts.query.filter_by(slug= post_slug).first()
    return render_template('post.html', post = post)

'''
- post_slug ye hamra banaya hua variable hai.(upr jo first line m likha hai vhoi hamra URL hoga vhi p ye kam krega.)
- hmne ek (post) nam ka variable bnaya hai jisme us perticular table ka fetch hoga.
- Post.query.filter_by() ye ek method hai jisse hm koi bhi value fetch krwa skte hai.
- ab (slug = post_slug) isme jo (slug) hai vo to databse ka hai, or post_slug hmara banaya hua hai.
- ab jab hm us URL ko hit krenge tab post_slug k ander post ka name aajaega ,fir vo value database k slug k sath check krenge,ar hmko vo data fetch krk ladega.
- first() fuction hm isiliye use krte hai, kuki database m phla post us slug m milega vo fetch ho jaega.
'''


#---------------------------------------------------------------------------------------------------------------------------

@app.route("/edit/<string:sno>", methods= ['GET', 'POST'])
def edit(sno):
    if ('user' in session and session['user'] == "harsh"):
        if request.method == 'POST':
            box_title= request.form.get('title')
            box_slug= request.form.get('slug')
            box_content= request.form.get('content')
            box_img_file= request.form.get('img_file')


            if sno =='0':
                post = Posts(title= box_title, slug= box_slug, content= box_content,img_file=box_img_file, date = datetime.now())
                db.session.add(post)
                db.session.commit()
            else:
                post = Posts.query.filter_by(sno=sno).first()
                post.title = box_title
                post.slug = box_slug
                post.content = box_content
                post.img_file = box_img_file
                db.session.commit()
                return redirect('/edit/'+sno)

        post = Posts.query.filter_by(sno=sno).first()
        return render_template('edit.html',post=post,sno=sno)




#-------------------------------------------------------------------------------------------------------------------


@app.route("/logout")
def logout():
    session.pop('user')
    return redirect('/dashboard')


@app.route("/delete/<string:sno>", methods= ['GET', 'POST'])
def delete(sno):
    if ('user' in session and session['user'] == "harsh"):
        post= Posts.query.filter_by(sno= sno).first()
        db.session.delete(post)
        db.session.commit()
    return redirect('/dashboard')
#-----------------------------------------------------------------------------------------


@app.route("/contact", methods= ['GET','POST'])   #YE BLOCK HMKO DATABASE M ENTRY KRWANE K KAM ATA HAI
def contact():
    if (request.method == 'POST'):         # ye shuro krne se phle hmko html me sb inputs ko name dene pdenge .
                                           # fir name dene k bad same name k variable bnaenge(LHS) m jo hai same.
        name=request.form.get('name')      # request ek module hai jisko hmko import krna pdta hai flask m
        email=request.form.get('email')    # request.form.get() method hai jisse hm value insert krne k lie use krenge.
        phone=request.form.get('phone')    # right side m jo () m hai jo sare name hi hai jo hmne html m die hai.
        message=request.form.get('message') # jb hm form m value bhrenge tab vo values yha se send hok entry variable m jaengi

        entry = Contacts(name=name, phone_num=phone, msg= message,date = datetime.now(), email=email)
        db.session.add(entry)            # entry k ander hm apni values database m dalenge
        db.session.commit()              # db.session.add(entry) or db.session.commit() ye dono  syntax fixed hai

    return render_template('contact.html')





app.run(debug=True)


#-----------------------------------------------------------------------------------------------------------------------------








