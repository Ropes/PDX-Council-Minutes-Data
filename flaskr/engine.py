from __future__ import unicode_literals, print_function

from flask import (Flask, request, session, g, redirect, url_for, 
        abort, render_template, flash)

from orm.conn import connect_engine, make_session
from orm.tables import Base, Meetingdate, Token, Tokenlink 
from flaskr.queries import *

engine = connect_engine()
session = make_session(engine)

app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True

@app.route("/")
def root():
    return render_template("index.html", title="PDX Council Minute Token Graphs")

@app.route("/doc/<id>/<token>")
def search(id, token):

    cursor = session.execute(token_query2, {'token': token, 'id': id})
    rows = cursor.fetchall()

    return render_template("token.html",
            title="Text Token Graphs",
            id=id,
            token=token,
            rows=rows)

if __name__ == '__main__':
    app.run()

