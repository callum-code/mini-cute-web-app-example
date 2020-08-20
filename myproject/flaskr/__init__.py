import os

from flask import Flask, request, render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def homepage():
        return render_template('index.html')

    @app.route('/user_form')
    def load_inputs():
        data = "hello I'm some useful data"
        fields = (
          ("0", "--NOU--", "Please enter a noun"),
          ("1", "--ADJ--", "Please enter an adjective"),
          ("2", "--VRB--", "Please enter a verb")
        )
        return render_template('user_form.html', fields=fields, some_data=data)

    @app.route('/submit_form', methods=('GET', 'POST'))
    def submit():
        stringy=""
        data=request.form["DataString"]
        keys={"--NOU--_0", "--ADJ--_1", "--VRB--_2"}
        for key in keys:
            stringy = stringy + "(" + key + ", " + request.form[key] + "), "
        display_text="passed data: " + data + "\nuser data: " + stringy
        return render_template('submit.html', user_text=display_text)

    return app
