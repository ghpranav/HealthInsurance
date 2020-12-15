from flask import Flask, render_template, json, request, redirect, url_for, flash
from flaskext.mysql import MySQL
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import uuid

def create_app():
    """Function to create and return an application"""
    app = Flask(__name__, static_url_path="/static")
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

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
        # return render_template("index.html")

    
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
            data = cur.fetchone()
            custID = int(data[0])
            # print(int(custID[0]))
            cur.execute("INSERT INTO Address VALUES (%s, %s, %s, %s, %s)", (custID, doorno, street, city, state))

            startDate = date.today()
            renewalDate = startDate + relativedelta(years = 1)
            policyNo = str(uuid.uuid4().int)[:10]
            # print(startDate, renewalDate, str(uuid.uuid1().node))
            cur.execute("INSERT INTO Holds VALUES (%s, %s, %s, %s, %s)", (custID, policyID, policyNo, str(startDate), str(renewalDate)))
            

            # mysql.connection.commit()
            conn.commit()
            cur.close()
            conn.close()
            flash("Succesfully bought Policy No. " + policyNo + " for Customer ID " + str(custID), 'msg')
            return redirect(url_for('index'))
        return render_template("buy.html", policyID=policyID)

    @app.route("/claim", methods=['GET', 'POST'])
    def claim():
        if request.method == "POST":
            details = request.form
            custID = details['custID']
            policyNo = details['policyNo']
            disease = details['disease']
            hospital = details['hospital']
            hospID = details['hospID']
            bill = details['bill']
            issuedAmt = str(.75 * int(bill))
            currYr = datetime.now().year

            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("INSERT into hospital values (%s, %s, %s, %s)", (hospital, hospID, custID, bill))
            cur.execute("INSERT into diagnosedby values (%s, %s, %s)", (disease, hospID, custID))
            cur.execute("INSERT into claims values (%s, %s, %s, %s)", (custID, policyNo, issuedAmt, currYr))
            conn.commit()

            cur.close()
            conn.close()
            flash("Succesfully claimed Policy No. " + policyNo + " for Rs. " + issuedAmt, 'msg')
            return redirect(url_for('index'))
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
    
    @app.route("/policy", methods=['GET', 'POST'])
    def policy():
        if request.method == "POST":
            details = request.form
            custID = details['custID']
            policyNo = details['policyNo']

            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("SELECT c.First_name, c.Last_name,i.Name as Policyname,h.Policy_number, h.Renewal_date, i.premium FROM customers c, holds h,insurance_policy i where c.Customer_id=%s and h.Policy_number=%s and h.PolicyID=i.PolicyID", (custID, policyNo))
            data = cur.fetchone()
            cur.close()
            conn.close()
            return render_template("display.html", data=data)
        return render_template("policy.html")

    @app.route("/display")
    def display(data):
        return render_template("display.html", data=data)

    app.debug = True
    return app
