from __future__ import unicode_literals, print_function

from flask import (Flask, request, session, g, redirect, url_for, 
        abort, render_template, flash)

import orm

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/")
def root():
    return render_template("index.html")

if __name__ == '__main__':
    app.run()
