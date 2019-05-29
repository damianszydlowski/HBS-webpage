from main import db
import datetime


class Guest(db.Model):
    __tablename__ ="guests"
    id = db.Column("GuestID", db.Integer, primary_key=True)
    email = db.Column("Email", db.String)
    password = db.Column("Password", db.String)
    name = db.Column("FirstName", db.String)
    surname = db.Column("LastName", db.String)
    phone1 = db.Column("Phone1", db.Integer)
    phone2 = db.Column("Phone2", db.Integer)
    address = db.Column("Address", db.String)
    city = db.Column("City", db.String)
    zip_code = db.Column("ZipCode", db.String)
    country = db.Column("Country", db.String)
    authenticated = db.Column("isAuth", db.Boolean, default=False)
    activated = db.Column("Active", db.Boolean, default=False)
    created = db.Column("CreatedAt", db.Date, default=datetime.datetime.now, onupdate=datetime.datetime.now)

    def __repr__(self):
        return '<User {}>'.format(self.email)

    def is_active(self):
        return self.activated

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def check_password(self, passwd):
        return self.password == passwd


class Room(db.Model):
    __tablename__ ="rooms"
    id = db.Column("RoomID", db.Integer, primary_key=True)
    number = db.Column("RoomNumber", db.Integer)
    subrooms = db.Column("SubRooms", db.Integer)
    bed1ppl = db.Column("Bed1ppl", db.Integer)
    bed2ppl = db.Column("Bed2ppl", db.Integer)
    kitchen = db.Column("Kitchen", db.Boolean)
    minibar = db.Column("Minibar", db.Boolean)
    size_m2 = db.Column("Sizem2", db.Integer)
    type_id = db.Column("RoomTypeID", db.Integer, db.ForeignKey("RoomType.id"), nullable=False)
    price = db.Column("Price", db.Integer)
    type_name = ""

    def __repr__(self):
        return '<Room {}>'.format(self.number)


class RoomType(db.Model):
    __tablename__ = "roomtypes"
    id = db.Column("RoomTypeID", db.Integer, primary_key=True)
    name = db.Column("RoomTypeName", db.String)

    def __repr__(self):
        return '<RoomType {}>'.format(self.name)


class Reservation(db.Model):
    __tablename__ ="reservations"
    id = db.Column("ReservationID", db.Integer, primary_key=True)
    guest_id = db.Column("GuestID", db.Integer, db.ForeignKey("guests.GuestID"), nullable=False)
    room_id = db.Column("RoomID", db.Integer, db.ForeignKey("rooms.RoomID"), nullable=False)
    date_from = db.Column("DateFrom", db.Date)
    date_to = db.Column("DateTo", db.Date)
    confirmed = db.Column("IsConfirmed", db.Boolean)
    people = db.Column("PplNumber", db.Integer)
    breakfasts = db.Column("Breakfasts", db.Integer, default=0)
    dinners = db.Column("Dinners", db.Integer, default=0)
    suppers = db.Column("Suppers", db.Integer, default=0)
    
    def __repr__(self):
        return '<Reservation {}:{}>'.format(self.guest_id, self.room_id)

    def available(self,desired_date_from, desired_date_to):
        return ((desired_date_from <= self.date_from and desired_date_to <= self.date_from) or
                    (desired_date_from >= self.date_to and desired_date_to >= self.date_to))
