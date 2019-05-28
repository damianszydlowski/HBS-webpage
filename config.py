#DB-Config
host = "127.0.0.1"
user = "web_client"
password = "hbs-web_c1"
db_name = "hbs"

class FlaskConfig():
    SECRET_KEY = "hbs-secret-lol"
    SQLALCHEMY_DATABASE_URI =  "mysql+pymysql://" + user + ":" + password + "@" + host + "/" + db_name
    SQLALCHEMY_TRACK_MODIFICATIONS = True
