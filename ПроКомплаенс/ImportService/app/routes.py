from flask import render_template, flash, redirect, url_for, request, g
from app import app, db
from app.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, AddFileForm
from app.models import User, Files
from app.emailf import send_password_reset_email
from flask_babel import _, get_locale
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
import pandas as pd
import chardet, json

@app.before_request
def before_request():
    g.locale = str(get_locale()) 
    
prefix = 'LKDB_'



@app.route('/', methods = ['GET', 'POST'])
@app.route('/index', methods = ['GET', 'POST'])
def index():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    if request.method == 'POST' and request.data:
        parsed_data = json.loads(request.data.decode('utf8'))
        if parsed_data['do'] == 'delete':
            db.session.execute(f"Drop table '{parsed_data['tablename']}';")
            db.session.commit()
            db.session.execute(f"Delete from files where file_name='{parsed_data['tablename']}';")
            db.session.commit()
            flash('Файл успешно удалён!')
            return redirect(url_for('index'))
        if parsed_data['do'] == 'show':
            return redirect(url_for("table", tablename=parsed_data['tablename']))

    form = AddFileForm()
    if form.validate_on_submit():
        new_file_name = form.fileContents.data.filename#.replace('.csv', '')
        if Files.query.filter_by(file_name = new_file_name).first():
            flash('Файл с таким названием уже загружен!')
        else:
            file = Files(file_name= new_file_name)
            file_data = request.files['fileContents']
            file_data.seek(0)
            encoding = chardet.detect(file_data.read())['encoding']
            file_data.seek(0)
            df = pd.read_csv(file_data, encoding=encoding)
            if 'index' in df.columns.str.lower():
                df.rename(columns={'index': prefix+'index', 'Index': prefix+'Index'}, inplace=True)
            df.to_sql(new_file_name, con=db.engine, if_exists = "replace")
            db.session.add(file)
            db.session.commit() 
            flash('Файл успешно загружен!')
            return redirect(url_for('index'))
        
    files_data = {}
    for f in Files.query.all():
        column_info = db.session.execute(f"PRAGMA table_info('{f.file_name}');").all()
        files_data[f.file_name] = [col.name.replace(prefix, '') for col in column_info[1:]]
    return render_template('index.html', title = 'ImportService', form = form, files_data=files_data) 


@app.route('/table/<tablename>', methods = ['GET'])
def table(tablename):
    column_info = db.session.execute(f"PRAGMA table_info('{tablename}');").all()
    column_names = [col.name.replace(prefix, '') for col in column_info[1:]]
    all_items = db.session.execute(f"Select * from '{tablename}';").all()
    return render_template('table.html', title = tablename, column_names=column_names, all_items = all_items) 



@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Поздравляем, теперь Вы зарегистрированы!')
        return redirect(url_for('login'))
    return render_template('register.html', title = _('Register'), form = form)


@app.route('/reset_password_request', methods = ['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            return send_password_reset_email(user)
        #flash('Проверьте свой email с дальнейшими инструкциями по сбросу пароля')
        #return redirect(url_for('login'))
    return render_template('reset_password_request.html', form = form,title = 'Сброс пароля')


@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Ваш пароль был сброшен')
        return redirect(url_for('login'))
    return render_template('reset_password.html', title =  'Сброс пароля',
                           form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Неверное имя пользователя или пароль')
            return redirect(url_for('login'))
        login_user(user, remember = form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title = 'Войти', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))