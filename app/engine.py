from __future__ import unicode_literals, print_function

from flask import Flask

import orm

app = Flask(__name__)

@app.route("/")
def root():
    return "Hellow!"

if __name__ == '__main__':
    app.run()
