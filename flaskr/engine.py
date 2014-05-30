from __future__ import unicode_literals, print_function

from flask import (Flask, request, session, g, redirect, url_for, 
        abort, render_template, flash)

from orm.tables import Base, Meetingdate, Token, Tokenlink 
from orm.conn import connect_engine, make_session

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

@app.route("/")
def root():
    return render_template("index.html", title="PDX Council Minute Token Graphs")

if __name__ == '__main__':
    app.run()

