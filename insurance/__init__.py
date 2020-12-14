from flask import Flask, render_template, json, request, redirect, url_for
from flaskext.mysql import MySQL

def create_app():
    """Function to create and return an application"""
    app = Flask(__name__, static_url_path="/static")
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'ghpranav'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'pranav123'
    app.config['MYSQL_DATABASE_DB'] = 'Health_Insurance'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    mysql.init_app(app)

    @app.route("/")
    def index():
        try:
            conn = mysql.connect()
            cursor =conn.cursor()

            cursor.execute("SELECT * from Customers")
            data = cursor.fetchone()
            return render_template("index.html")
        except Exception as e:
            return json.dumps({'error':str(e)})
        finally:
            cursor.close() 
            conn.close()
    
    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/buy/<policyID>", methods=['GET', 'POST'])
    def buy(policyID):
        if request.method == "POST":
            details = request.form
            fname = details['fname']
            lname = details['lname']
            dob = details['dob']
            phone = details['phone']
            doorno = details['doorno']
            street = details['street']
            city = details['city']
            state = details['state']

            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("INSERT INTO Customers(First_name, Last_name, Birth_date, Phone) VALUES (%s, %s, %s, %s)", (fname, lname, dob, phone))
            cur.execute("SELECT Customer_id FROM Customers ORDER BY Customer_id DESC LIMIT 1;")
            custID = cur.fetchone()
            # print(int(custID[0]))
            cur.execute("INSERT INTO Address VALUES (%s, %s, %s, %s, %s)", (int(custID[0]), doorno, street, city, state))
            # cur.execute("INSERT INTO Holds(Customer_id, PolicyID, Start_date, Renewal_date) VALUES (%s, %s, %s)", (int(custID[0]), ))
            

            # mysql.connection.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        return render_template("buy.html", policyID=policyID)

    @app.route("/claim")
    def claim():
        return render_template("claim.html")

    @app.route("/contact")
    def contact():
        return render_template("contact.html")

    @app.route("/insurance")
    def insurance():
        return render_template("insurance.html")

    @app.route("/resource")
    def resource():
        return render_template("resource.html")
    
    @app.route("/policy")
    def policy():
        return render_template("policy.html")

    app.debug = True
    return app
