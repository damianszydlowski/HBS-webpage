from main import app
from flask import request, flash, url_for, redirect, render_template
from flask_login import login_user, logout_user, login_required, current_user
from models import *
from datetime import datetime, timedelta

#strings
pageTypes = {"all": "Wszystkie pokoje", "available": "Tylko dostępne pokoje", "dates": "Z podanego przedziału"}
date_format = "%Y-%m-%d"

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


@app.route('/book',  methods=['GET', 'POST'])
def book():
    if request.method == 'GET':
        date_from = datetime.now()
        date_to = date_from + timedelta(days=3)
        return render_template('book.html', date_from=date_from, date_to=date_to)
    date_from = request.form['date-from']
    date_to = request.form['date-to']
    people_number = request.form['ppl']
    return redirect("/search/from={}&to={}&ppl={}".format(date_from, date_to, people_number))


@app.route('/search/from=<date_from>&to=<date_to>&ppl=<ppl>', methods=['GET', 'POST'])
@login_required
def list_rooms_dates(date_from, date_to, ppl):
    date_from = datetime.strptime(date_from, date_format).date()
    date_to = datetime.strptime(date_to, date_format).date()
    reservations = Reservation.query.all()
    booked = []
    for res in reservations:
        if not res.available(date_from, date_to):
            booked.append(res.room_id)
    rooms = Room.query.filter(~Room.id.in_(booked))
    rooms_with_desc = []
    for r in rooms:
        r.type_name = RoomType.query.filter_by(id=r.type_id).first().name
        rooms_with_desc.append(r)
    if request.method == 'GET':
        return render_template("choose_room.html", date_from=date_from, date_to=date_to, result=rooms_with_desc)
    room_id = request.form['choose_room']
    reservation = Reservation(
        guest_id = current_user.id,
        room_id = room_id,
        date_from = date_from,
        date_to = date_to,
        confirmed = False,
        people = ppl
    )
    db.session.add(reservation)
    db.session.commit()
    flash('Pomyślnie zarezerwowano!'.format(current_user.name))
    return redirect(url_for('user_panel'))


@app.route('/rooms/<type>')
@login_required
def list_rooms(type):
    rooms = []
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
    t = Reservation.query.filter_by(guest_id=current_user.id).order_by(Reservation.id.desc())
    reservations = []
    for res in t:
        room = Room.query.filter_by(id=res.room_id).first()
        res.room_number = room.number
        res.room_type = RoomType.query.filter_by(id=room.type_id).first().name
        res.room_price = room.price
        res.room_price_total = abs((res.date_to - res.date_from).days)*room.price
        reservations.append(res)
    # return render_template("user_panel.html", has_reservation = has_reservation, res_info = res_info)

    return render_template("user_panel.html", reservations = reservations)
