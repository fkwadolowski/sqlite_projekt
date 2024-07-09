from flask import Flask, render_template, request, redirect, url_for

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)

all_books = []


@app.route('/')
def home():
    return render_template("index.html",data=all_books)


@app.route("/add", methods=['post', 'get'])
def add():
    data = request.form
    if request.method == "POST":
        dict_data = {
            'title': data['title'].title(),
            'author': data['author'].title(),
            'rating': int(data['rating']),
        }
        all_books.append(dict_data)
        return redirect(url_for('home'))

    return render_template('add.html')


if __name__ == "__main__":
    app.run(debug=True)
