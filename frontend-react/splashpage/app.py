from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/', methods=['GET', 'POST'])
def splash():
    error_message = None

    if request.method == 'POST':
        student_id = request.form.get('student_id')

        # Validate input: Only allow 4-digit numbers
        if student_id and student_id.isdigit() and len(student_id) == 4:
            session['student_id'] = student_id  # Store ID in session
            return redirect(url_for('home'))
        else:
            error_message = "Invalid ID! Please enter a 4-digit number."

    return render_template('splash.html', error_message=error_message)

@app.route('/home')
def home():
    student_id = session.get('student_id', 'Unknown')
    return render_template('home.html', student_id=student_id)

if __name__ == '__main__':
    app.run(debug=True)
