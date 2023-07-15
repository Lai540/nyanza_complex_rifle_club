from flask import Flask, render_template, request, redirect, g
import sqlite3

app = Flask(__name__)

DATABASE = 'club_database.db'

# Helper function to get the database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

# Close the database connection at the end of each request
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# Create the members table if it doesn't exist
def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS members (
                        member_number INTEGER,
                        name TEXT NOT NULL,
                        postal_address TEXT NULL,
                        fc_no TEXT NULL,
                        id_number INTEGER PRIMARY KEY,
                        county TEXT NOT NULL,
                        telephone TEXT NULL,
                        email TEXT NULL,
                        membership_category TEXT NULL,
                        spouse TEXT NOT NULL,
                        Spouse_contact TEXT NULL,
                        company TEXT NOT NULL,
                        proposer TEXT NOT NULL
                        )''')
        db.commit()


# Initialize the database
init_db()

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Add member route
@app.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        # Handle form submission and database insertion
        # ...

        return redirect('/members')

    return render_template('add_member.html')

# Update member route
@app.route('/update_member', methods=['GET', 'POST'])
def update_member():
    if request.method == 'POST':
        member_number = request.form['member_number']

        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM members WHERE member_number=?", (member_number,))
        member = cursor.fetchone()

        if member:
            return render_template('update_member.html', member=member)
        else:
            return "Member not found!"

    return render_template('index.html')

# Update member details route
@app.route('/update_member_details', methods=['POST'])
def update_member_details():
    member_number = request.form['member_number']
    name = request.form['name']
    postal_address = request.form['postal_address']
    fc_no = request.form['fc_no']
    id_number = request.form['id_number']
    county = request.form['county']
    telephone = request.form['telephone']
    email = request.form['email']
    membership_category = request.form['membership_category']
    spouse = request.form['spouse']
    Spouse_contact = request.form['Spouse_contact']
    company = request.form['company']
    proposer = request.form['proposer']

    db = get_db()
    cursor = db.cursor()

    cursor.execute("UPDATE members SET name=?, postal_address=?, fc_no=?, id_number=?, county=?, telephone=?, email=?, membership_category=?, spouse=?, Spouse_contact=?, company=?, proposer=? WHERE member_number=?", (name, postal_address, fc_no, id_number, county, telephone, email, membership_category, spouse, Spouse_contact, company, proposer, member_number))
    db.commit()

    return redirect('/members')

# View members route
@app.route('/members')
def view_members():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    return render_template('view_members.html', members=members)

# View member details by ID route
@app.route('/member_details', methods=['GET'])
def member_details():
    member_number = request.args.get('member_number')

    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM members WHERE member_number=?", (member_number,))
    member = cursor.fetchone()

    if member:
        return render_template('view_member.html', member=member)
    else:
        return "Member not found!"

# Remove member route
@app.route('/remove_member/<int:id_number>')
def remove_member(id_number):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM members WHERE id_number =?", (id_number,))
    db.commit()

    return redirect('/members')

# Home page
@app.route('/home')
def homepage():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
