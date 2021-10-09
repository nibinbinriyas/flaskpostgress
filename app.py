
from flask import  render_template,redirect,url_for,request,flash
from baseapp.models import Book
from baseapp.forms import AddForm
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





if __name__ == '__main__':
    app.run(debug=True)