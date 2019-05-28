from main import app
from flask import request, flash, url_for, redirect, render_template
from flask_login import login_user, logout_user, login_required, current_user
from models import *

#strings
pageTypes = {"all": "Wszystkie pokoje", "available": "Tylko dostępne pokoje"}


@app.route("/")
def home():
    return render_template('home.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    email = request.form['email']
    guest = Guest.query.filter_by(email=email).first()
    if guest is not None:
        flash('Już posiadasz konto. Zaloguj się', 'error')
        return redirect(url_for('login'))
    password = request.form['password']
    if password != request.form['password2']:
        flash('Hasła nie są takie same', 'error')
        return redirect(url_for('register'))
    name, surname = request.form['name'], request.form['surname']
    phone1, phone2 = request.form['phone1'], request.form['phone2']
    address = request.form['address']
    zip_code, city = request.form['zip_code'], request.form['city']
    country = request.form['country']
    guest = Guest(email = email,
                  password = password,
                  name = name,
                  surname = surname,
                  phone1 = phone1,
                  phone2 = phone2,
                  address = address,
                  zip_code = zip_code,
                  city = city,
                  country = country,
                  activated = True
                  )
    db.session.add(guest)
    db.session.commit()
    flash('Pomyślnie zarejestrowano. Teraz należy się zalogować.')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    password = request.form['password']
    remember_me = False
    if 'remember_me' in request.form:
        remember_me = True
    registered_user = Guest.query.filter_by(email=email).first()
    if registered_user is None:
        flash('Nieprawidłowa nazwa użytkownika', 'error')
        return redirect(url_for('login'))
    if not registered_user.check_password(password):
        flash('Nieprawidłowe hasło', 'error')
        return redirect(url_for('login'))
    print (registered_user)
    login_user(registered_user, remember=remember_me)
    flash('Pomyślnie zalogowano. Witaj, {}'.format(current_user.name))
    return redirect(request.args.get('next') or url_for('home'))


@app.route('/logout')
def logout():
    logout_user()
    flash('Pomyślnie wylogowano.')
    return redirect(url_for('home'))


@app.route("/rooms/<type>")
@login_required
def list_rooms(type):
    if type == "all":
        rooms = Room.query.all()
    elif type == "available":
        reserved = db.session.query(Reservation.room_id)
        rooms = Room.query.filter(~Room.id.in_(reserved))
    for room in rooms:
        room.type_name = RoomType.query.filter_by(id=room.type_id).first().name
    return render_template("rooms.html", pageType=pageTypes[type], result=rooms, content_type="application/json")


@app.route("/user-panel")
@login_required
def user_panel():
    res_info = Reservation.query.filter_by(guest_id=current_user.id).first()
    has_reservation = res_info is not None
    if has_reservation:
        room = Room.query.filter_by(id=res_info.room_id).first()
        res_info.room_number = room.number
        res_info.room_type = RoomType.query.filter_by(id=room.type_id).first().name
        res_info.room_price = room.price
    return render_template("user_panel.html", has_reservation = has_reservation, res_info = res_info)
