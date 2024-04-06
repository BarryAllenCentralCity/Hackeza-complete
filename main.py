from flask import Flask, render_template, redirect, url_for, request
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from io import BytesIO


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Connecting to DB
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///our_data.db"
db.init_app(app)


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
    c_date = db.Column(db.Integer, primary_key=True)
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
        the_user = USER_DETAIL.query.filter_by(email = form.email.data).first()

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
    return render_template("AdminPage.html")


@app.route('/admin_publication')
def admin_pub_page():
    return render_template("AdminPublicationPage.html")


@app.route('/entries')
def entries():
    return render_template("EntriesPage.html")


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
        

        # Process the form data here, you can save it to database or perform other actions
        # For now, let's just print the values
        # print(f"Publication Date: {publication_date}")
        # print(f"National/International: {national_international}")
        # print(f"Ranking: {ranking}")
        # print(f"Broad Area: {broad_area}")
        # print(f"Paper Title: {paper_title}")
        # print(f"Conference Name: {conference_name}")
        # print(f"Impact Factor: {impact_factor}")
        # print(f"Conference Location: {conference_location}")
        # print(f"Volume: {volume}")
        # print(f"Issue: {issue}")
        # print(f"Page Numbers: {page_numbers}")
        # print(f"DOI: {doi}")
        # print(f"Publisher: {publisher}")
        # print(f"Authors: {authors}")
        new_journal = JOURNALS(
            j_email="j_email",
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
            j_con_loc = conference_location
        )

        # Add the new_journal to the database session
        db.session.add(new_journal)

        # Commit the changes to persist them in the database
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template("JournalPage.html")


@app.route('/conference', methods=["GET", "POST"])
def conference():
    if request.method == "POST":
        # Extract form data
        c_email = "c_mail"
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
        return redirect(url_for('home_page'))
    return render_template("ConferencePage.html")


@app.route('/publication_edit')
def pub_edit_page():
    return render_template("PublicationEditPage.html")




if __name__ == "__main__":
    app.run(debug=True)
