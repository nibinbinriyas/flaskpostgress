
from flask import  render_template,redirect,url_for,request,flash
from baseapp.models import Book
from baseapp import app,db







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
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            
            login_user(user)
            flash('Logged in successfully')

            next = request.args.get('next')

            if next == None or not next[0] == '/':
                next = url_for('index')
            return redirect(next)

    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        
        db.session.add(user)
        db.session.commit()
        flash('Successfully Registered!')

        return redirect(url_for('login'))
    
    return render_template('register.html',form=form)



if __name__ == '__main__':
    app.run(debug=True)