from flask import render_template, flash, redirect, url_for
from flask_login import login_user, logout_user
from app import app, db, lm

from app.models.tables import User
from app.models.forms import LoginForm, RegisterForm


@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/", methods=["GET","POST"])
def index():
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.username.data).first()
		if user and user.password == form.password.data:
			login_user(user)
			return redirect(url_for("dashboard"))
		else :
			flash("invalido")

		"""if user:
			if user.password == form.password.data:
				print ("GG")
			else:
				print ("nãotãoruim")
		else:
			print ("deuruim")"""		
		
	return render_template('index.html',
								form=form)

@app.route("/login", methods=["GET","POST"])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.username.data).first()
		if user and user.password == form.password.data:
			login_user(user)
			return redirect(url_for("dashboard"))
		else :
			flash("invalido")
	return render_template('login.html',form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("index"))

@app.route("/dashboard", methods=["GET","POST"])
def dashboard():
	return render_template('dashboard.html')

"""@app.route("/register", methods=["GET","POST"])
def register():
	form=RegisterForm()
	if form.validate_on_submit():
		email = form.email.data
		nome = form.nome.data
		if email == nome:
			return print(nome)
		else:
			return print(nome)
	#db.session.add(i)
	#db.session.commit()
	return render_template('register.html', form=form)"""

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(form.nome.data, form.sobrenome.data, form.email.data,
                    form.password.data)
        db_session.add(user)
        flash('Thanks for registering')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/maps")
def maps():
    return render_template("maps.html")

@app.route("/upload", methods=["POST"])
def upload():
    """Handle the upload of a file."""
    form = request.form

    # Cria um Id particular para essa sessao de upload
    upload_key = str(uuid4())

    # Is the upload using Ajax, or a direct POST by the form?
    is_ajax = False
    if form.get("__ajax", None) == "true":
        is_ajax = True

    # Target folder for these uploads.
    target = "uploadr/static/uploads/{}".format(upload_key)
    try:
        os.mkdir(target)
    except:
        if is_ajax:
            return ajax_response(False, "Couldn't create upload directory: {}".format(target))
        else:
            return "Couldn't create upload directory: {}".format(target)

    print("=== Form Data ===")
    for key, value in list(form.items()):
        print(key, "=>", value)

    for upload in request.files.getlist("file"):
        filename = upload.filename.rsplit("/")[0]
        destination = "/".join([target, filename])
        print("Accept incoming file:", filename)
        print("Save it to:", destination)
        upload.save(destination)

    if is_ajax:
        return ajax_response(True, upload_key)
    else:
        return redirect(url_for("upload_complete", uuid=upload_key))

@app.route("/files")
def files():
    return render_template("files.html")    



@app.route("/files/<uuid>")
def upload_complete(uuid):
    """The location we send them to at the end of the upload."""

    # Get their files.
    root = "uploadr/static/uploads/{}".format(uuid)
    if not os.path.isdir(root):
        return "Error: UUID not found!"

    files = []
    for file in glob.glob("{}/*.*".format(root)):
        fname = file.split(os.sep)[-1]
        files.append(fname)

    return render_template("files.html",
        uuid=uuid,
        files=files,
    )


def ajax_response(status, msg):
    status_code = "ok" if status else "error"
    return json.dumps(dict(
        status=status_code,
        msg=msg,
    ))

