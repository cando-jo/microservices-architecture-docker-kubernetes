import jwt, datetime ,os
from flask import Flask, request
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)ss

server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")

@server.route("/login", methods=['POST'])
def login():
    auth = request.autharization
    if not auth:
        return "Missing credintials", 401

    cur = mysql.connection.cursor()
    res = cur.exectue(
	"SELECT email, password FROM user WHERE email=%s", (auth.username),
    )
	
    if res > 0:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credintials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)

    else:
    	return "Invalid credentials", 401

def createJWT(username, secret, authz):
    return jwt.encode(
            {"username": username, 
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(days=1),
            "iat": datetime.datetime.utcnow(),
            "admin": authz,
            },
            secret ,
            algorithm="HS256"
            )

@server.route('/validate')
def validate():
    encoded_jwt = request.headers['Authorization']
    if not encoded_jwt:
        return "Missing credentials", 401
    encoded:jwt = encoded_jwt.split(" ")[1]
    try:
        decoded = jwt.decote(
            encoded_jwt, os.environ.get("JWT_SECRET", algorithm=['HS256'])
        )
    except:
        return "not authorized", 403

    return decoded, 200
if __name__ == "__main__":
    server.run(host='0.0.0.0', port=5052)

