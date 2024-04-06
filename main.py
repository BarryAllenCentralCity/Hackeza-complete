import os
import smtplib

from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Connecting to DB
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///our_data.db"
db.init_app(app)

login_id = ""
ADMIN_EMAIL = os.environ.get('email')
PASSWORD = os.environ.get('password')


class USER_DETAIL(db.Model):
    __tablename__ = "user_detail"
    email = db.Column(db.String(120), unique=True, nullable=False, primary_key=True)
    roles = db.Column(db.String(120), nullable=False)


class JOURNALS(db.Model):
    __tablename__ = "journals"
    j_email = db.Column(db.String(120), nullable=False)
    j_dop = db.Column(db.String(20), nullable=False)
    j_nat_inat = db.Column(db.String(120), nullable=False)
    j_ranking = db.Column(db.Integer, nullable=False)
    j_broad_area = db.Column(db.String(120), nullable=False)
    j_con_name = db.Column(db.String(120))
    j_impf = db.Column(db.String(120), nullable=False)
    j_pap_tit = db.Column(db.String(120), nullable=False)
    j_doi = db.Column(db.String(120), nullable=False, primary_key=True)
    j_authors = db.Column(db.String(200), nullable=False)
    j_volume = db.Column(db.String(120), nullable=False)
    j_issue = db.Column(db.String(120), nullable=False)
    j_page_n = db.Column(db.String(120), nullable=False)
    j_publisher = db.Column(db.String(120), nullable=False)
    j_con_loc = db.Column(db.String(120), nullable=False)


class CONFERENCE(db.Model):
    __tablename__ = "conference"
    c_email = db.Column(db.String(120), nullable=False)
    c_date = db.Column(db.Integer, nullable=False)
    c_nat = db.Column(db.String(120), nullable=False)
    c_corerank = db.Column(db.Integer, nullable=False)
    c_pap_tit = db.Column(db.String(120), nullable=False)
    c_short_name = db.Column(db.String(120), nullable=False)
    c_con_location = db.Column(db.String(120), nullable=False)
    c_full_name = db.Column(db.String(120), nullable=False)
    c_url = db.Column(db.String(120), nullable=False, primary_key=True)
    c_authors = db.Column(db.String(200), nullable=False)
    c_volume = db.Column(db.String(120), nullable=False)
    c_issue = db.Column(db.String(120), nullable=False)
    c_page_n = db.Column(db.String(120), nullable=False)
    c_publisher = db.Column(db.String(120), nullable=False)


with app.app_context():
    db.create_all()


# db.create_all()

@app.route('/')
def login_page():
    return render_template("LoginPage.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Process the form data here
        the_user = USER_DETAIL.query.filter_by(email=form.email.data).first()

        if the_user:

            if the_user.roles == 'admin':
                return redirect(url_for('admin_page'))

            else:
                return redirect(url_for('home_page'))


        else:

            return redirect(url_for('unauthorized'))

        # print(form.email.data)
        # print(form.password.data)

        ##check in the data base##

        # if passed then the next line
        # if admin then pass then
        # return redirect(url_for('admin_page'))
        # else

        # else add the user in the database----------ye alag se function hoga...
        # else show unauthorised access
    return render_template('login.html', form=form)


@app.route('/home')
def home_page():
    return render_template("HomePage.html")


@app.route('/admin')
def admin_page():
    # taking in all the journal entries

    ##

    return render_template("AdminPage.html")


@app.route('/admin_publication')
def admin_pub_page():
    return render_template("AdminPublicationPage.html")


@app.route('/entries')
def entries():
    journals = JOURNALS.query.all()
    if journals:
        for journal in journals:
            print(journal.j_email)
            print(journal.j_con_name)
    else:
        print("NOTHING HERE")
    #####

    # taking in all the conference entries

    conferences = CONFERENCE.query.all()
    if conferences:
        for conference in conferences:
            print(conference.c_email)
            print(conference.c_nat)
    else:
        print("nothing here")
    return render_template("EntriesPage.html", journals=journals, conferences=conferences)


@app.route('/publication', methods=['GET', 'POST'])
def publication():
    return render_template("PublicationPage.html")


@app.route('/unauthorised')
def unauthorized():
    return render_template("UnauthorizedAccess.html")


@app.route('/journal', methods=["GET", "POST"])
def journal_page():
    if request.method == 'POST':
        publication_date = request.form['publication-date']
        national_international = request.form['national-international']
        ranking = request.form['ranking']
        broad_area = request.form['broad-area']
        paper_title = request.form['paper-title']
        conference_name = request.form['conference-name']
        impact_factor = request.form['impact-factor']
        conference_location = request.form['conference-location']
        volume = request.form['volume']
        issue = request.form['issue']
        page_numbers = request.form['page-numbers']
        doi = request.form['doi']
        publisher = request.form['publisher']
        authors = request.form['authors']

        new_journal = JOURNALS(
            j_email=login_id,
            j_dop=publication_date,
            j_nat_inat=national_international,
            j_ranking=ranking,
            j_broad_area=broad_area,
            j_con_name=conference_name,
            j_impf=impact_factor,
            j_pap_tit=paper_title,
            j_doi=doi,
            j_authors=authors,
            j_volume=volume,
            j_issue=issue,
            j_page_n=page_numbers,
            j_publisher=publisher,
            j_con_loc=conference_location
        )

        # Add the new_journal to the database session
        db.session.add(new_journal)

        # Commit the changes to persist them in the database
        db.session.commit()
        return "<h1>Entry done</h1>"
    return render_template("JournalPage.html", journal=None, IsEdit=False)


@app.route('/conference', methods=["GET", "POST"])
def conference():
    if request.method == 'POST':
        # Extract form data
        c_email = "maillll"
        c_date = request.form['conference-date']
        c_nat = request.form['type']
        c_corerank = request.form['corerank']
        c_pap_tit = request.form['title']
        c_short_name = request.form['shortname']
        c_con_location = request.form['location']
        c_full_name = request.form['fullname']
        c_url = request.form['url']
        c_authors = request.form['authors']
        c_volume = request.form['volume']
        c_issue = request.form['issue']
        c_page_n = request.form['pages']
        c_publisher = request.form['publisher']
        new_conference = CONFERENCE(
            c_email=c_email,
            c_date=c_date,
            c_nat=c_nat,
            c_corerank=c_corerank,
            c_pap_tit=c_pap_tit,
            c_short_name=c_short_name,
            c_con_location=c_con_location,
            c_full_name=c_full_name,
            c_url=c_url,
            c_authors=c_authors,
            c_volume=c_volume,
            c_issue=c_issue,
            c_page_n=c_page_n,
            c_publisher=c_publisher
        )

        # Add the new_conference to the database session
        db.session.add(new_conference)

        # Commit the session to persist the changes
        db.session.commit()
        return "<h1>Confrerece entry done</h1>"
    return render_template("ConferencePage.html", conference=None, IsEdit=False)


@app.route('/show_entry/<string:journal_doi>')
def show_entry(journal_doi):
    journal = JOURNALS.query.get(journal_doi)
    return render_template("ShowJournalPage.html", journal=journal)


@app.route('/show_conf_entry/<string:conf_url>')
def show_conf_entry(conf_url):
    conference = CONFERENCE.query.get(conf_url)
    return render_template("ShowConferencePage.html", conference=conference)


@app.route('/edit_journal/<string:journal_doi>', methods=['GET', 'POST'])
def edit_journal(journal_doi):
    journal = JOURNALS.query.get(journal_doi)
    # return "<h1>EDIT ME AAGYE</h1>"
    if request.method == 'POST':
        journal.j_dop = request.form['publication-date']
        journal.j_nat_inat = request.form['national-international']
        journal.j_ranking = request.form['ranking']
        journal.j_broad_area = request.form['broad-area']
        journal.j_pap_tit = request.form['paper-title']
        journal.j_con_name = request.form['conference-name']
        journal.j_impf = request.form['impact-factor']
        journal.j_volume = request.form['volume']
        journal.j_issue = request.form['issue']
        journal.j_page_n = request.form['page-numbers']
        journal.j_publisher = request.form['publisher']
        journal.j_authors = request.form['authors']

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('admin_pub_page'))
    return render_template("JournalPage.html", journal=journal, IsEdit=True)


@app.route('/edit_conference/<string:conf_url>', methods=['GET', 'POST'])
def edit_conference(conf_url):
    conference = CONFERENCE.query.get(conf_url)
    # return "<h1>EDIT ME AAGYE</h1>"
    if request.method == 'POST':
        conference.c_email = "maillll"
        conference.c_date = request.form['conference-date']
        conference.c_nat = request.form['type']
        conference.c_corerank = request.form['corerank']
        conference.c_pap_tit = request.form['title']
        conference.c_short_name = request.form['shortname']
        conference.c_con_location = request.form['location']
        conference.c_full_name = request.form['fullname']
        conference.c_url = request.form['url']
        conference.c_authors = request.form['authors']
        conference.c_volume = request.form['volume']
        conference.c_issue = request.form['issue']
        conference.c_page_n = request.form['pages']
        conference.c_publisher = request.form['publisher']

        # Commit the changes to the database
        db.session.commit()
        return redirect(url_for('admin_pub_page'))

    return render_template("ConferencePage.html", conference=conference, IsEdit=True)


@app.route('/delete_conference/<string:conf_url>')
def delete_conference(conf_url):
    conference = CONFERENCE.query.get(conf_url)
    db.session.delete(conference)
    db.session.commit()
    return redirect(url_for('entries'))


@app.route('/delete_journal/<string:journal_doi>')
def delete_journal(journal_doi):
    journal = JOURNALS.query.get(journal_doi)
    db.session.delete(journal)
    db.session.commit()
    return redirect(url_for('entries'))


@app.route('/send_mail')
def send_email():
    all_users = []
    total_users = USER_DETAIL.query.all()
    for user in total_users:
        if user.roles != 'admin':
            print(user.email)
            all_users.append(user.email)
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=ADMIN_EMAIL, password=PASSWORD)
        for email in all_users:
            connection.sendmail(from_addr=ADMIN_EMAIL, to_addrs=email,
                                msg=f"Subject:Regarding Journal or Conference Entry.\n\nPlease complete your entry in the portal to the earliest.")
    return redirect(url_for('admin_page'))


if __name__ == "__main__":
    app.run(debug=True)
