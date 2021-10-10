
from flask import  render_template,redirect,url_for,request,flash
from baseapp.models import Book,User
from baseapp import app,db
from flask_login.utils import login_required, login_user, logout_user






@app.route('/')
def index():
    books = Book.query.all()
    results = [
        {
            "name": book.name,
            "auther": book.auther,
            "price": book.price,
            "image":book.image
            
        } for book in books]
    return render_template('first.html',results=results)

@app.route('/home')
def home():
    books = Book.query.all()
    results = [
        {
            "name": book.name,
            "auther": book.auther,
            "price": book.price,
            "image":book.image
            
        } for book in books]
    return render_template('home.html',results=results)


@app.route('/add',methods=['GET','POST'])
def add():
    if request.method == 'POST':
        d = request.form.to_dict()
        name = d['name']
        auther = d['auther']
        price = d['price']
        image = d['image']
            
        new_book = Book(name, auther, price, image)
        db.session.add(new_book)
        db.session.commit()
        return {"message": f"car {new_book.name} has been created successfully."}

    
    elif request.method == 'GET':
        

        return render_template("add.html")

    else:
        return {"error": "The request payload is not in JSON format"}


@app.route('/delete',methods=['GET','POST'])
def delete():
    

    if request.method == 'POST':
        d = request.form.to_dict()
        id = d['id']
        book = Book.query.get(id)
        db.session.delete(book)
        db.session.commit()
        return redirect(url_for('index'))

    elif  request.method == 'GET':

        return render_template('delete.html')



@app.route('/search',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        d = request.form.to_dict()
        auther = d['auther']
        book_data = Book.query.all()

        return render_template('auther_books.html',book_data=book_data,auther=auther)
    elif request.method == 'GET':

        return render_template('search.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You are logged out")
    return redirect(url_for('index'))



@app.route('/login',methods=['GET','POST'])
def userlogin():
    

    if request.method == 'POST':
        d = request.form.to_dict()
        user = User.query.filter_by(email=d['email']).first()

        if user.check_password(d['password']) and user is not None:
            
            login_user(user)
            flash('Logged in successfully')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('home')
            return redirect(next)
    elif request.method == 'GET':
        return render_template('login.html')

@app.route('/register',methods=['GET','POST'])
def register():


    if request.method == 'POST':
        d = request.form.to_dict()
        user = User(email=d['email'],
                    username=d['username'],
                    password=d['password'])
        
        db.session.add(user)
        db.session.commit()
        flash('Successfully Registered!')

        return redirect(url_for('userlogin'))
    elif request.method == 'GET':

        return render_template('register.html')



if __name__ == '__main__':
    app.run(debug=True)