from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:/dynamic'
# Suppress deprecation warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize the SQLAlchemy instance
db = SQLAlchemy(app)


# Define a model for your form data
class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    names = db.Column(db.String(255))
    email = db.Column(db.String(255))
    department = db.Column(db.String(255))
    services = db.Column(db.String(255))
    status = db.Column(db.String(50))
    timeline = db.Column(db.String(50))
    on_boarded = db.Column(db.String(50))
    legal_instrument = db.Column(db.String(50))
    other_instrument = db.Column(db.String(255))
    changes_required = db.Column(db.String(3))
    change_details = db.Column(db.Text)
    services_to_enhance = db.Column(db.String(255))

    def __repr__(self):
        return f"<FormData {self.id}>"


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Access submitted data
    names = ', '.join(request.form.getlist('name[]'))
    email = request.form.get('email')
    department = request.form.get('department')
    services = request.form.get('services')
    status = request.form.get('status')
    timeline = request.form.get('timeline')
    on_boarded = request.form.get('on_boarded')
    legal_instrument = request.form.get('legal_instrument')
    other_instrument = request.form.get('other_instrument')
    changes_required = request.form.get('changes_required')
    change_details = request.form.get('change_details')
    services_to_enhance = request.form.get('services_to_enhance')

    # Create a new FormData instance
    new_data = FormData(
        names=names,
        email=email,
        department=department,
        services=services,
        status=status,
        timeline=timeline,
        on_boarded=on_boarded,
        legal_instrument=legal_instrument,
        other_instrument=other_instrument,
        changes_required=changes_required,
        change_details=change_details,
        services_to_enhance=services_to_enhance
    )

    # Add the new data to the database session
    db.session.add(new_data)
    # Commit the session to save changes to the database
    db.session.commit()

    # Return JSON response
    return jsonify(message="Your response has been recorded. Thank you!")


if __name__ == '__main__':
    # Create the database tables inside the application context
    with app.app_context():
        db.create_all()
    # Run the Flask application
    app.run(debug=True)
