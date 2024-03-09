from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/submit', methods=['POST'])
def submit():
    # Access submitted data
    names = request.form.getlist('name[]')
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

    # Save data to a text file
    with open('form_data.txt', 'a') as file:
        file.write(f"Name(s): {', '.join(names)}\n")
        file.write(f"Email: {email}\n")
        file.write(f"Department: {department}\n")
        file.write(f"Services offered: {services}\n")
        file.write(f"Current status: {status}\n")
        file.write(f"Timeline for digitizing manual services: {timeline}\n")
        file.write(f"On-boarded on E-Citizen platform: {on_boarded}\n")
        file.write(f"Guiding legal instrument/policy: {legal_instrument}\n")
        if legal_instrument == 'Others':
            file.write(f"Other legal instrument: {other_instrument}\n")
        file.write(f"Do changes required: {changes_required}\n")
        if changes_required == 'Yes':
            file.write(f"Changes required details: {change_details}\n")
        file.write(f"Services digitized but still need enhancements: {services_to_enhance}\n")
        file.write("\n")

    # Return JavaScript code for pop-up message
    return jsonify(message="Your response has been recorded. Thank you!")


if __name__ == '__main__':
    app.run(debug=True)
