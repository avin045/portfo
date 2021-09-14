from flask import Flask, render_template, send_from_directory, request, redirect
import csv
from mailer import Mailer

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route('/<string:pages>')
def all_pages(pages):
    return render_template(pages)


@app.route('/table_dAAA')
def pan():
    with open('db.csv', newline='\n') as csv_rec:
        print("functioning")
        results = []
        reader = csv.DictReader(csv_rec)
        print(reader)

        for row in reader:
            results.append(dict(row))
        return render_template('table_op.html', results=results)


def write_in_csv(data):
    with open('db.csv', newline='', mode='a') as db_csv:
        email = data['email']
        subject = data['subject']
        message = data['message']
        csv_db = csv.writer(db_csv, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        csv_db.writerow([email, subject, message])


def automatic_email(data_mail):
    user_mail = data_mail['email']
    mail = Mailer(email='blackkdevil786@gmail.com', password='PARker4566')
    mess = data_mail['message']
    msg = f"This person(Mail id) send message to you : \n \n \t {user_mail} \n \n The Message they entered is \n \n\t {mess}"
    mail.send(receiver='avinashsekar045@gmail.com', subject=data_mail['subject'], message=msg)


@app.route('/submit_form', methods=['POST', 'GET'])
def form():
    if request.method == 'POST':
        details = request.form.to_dict()
        print(details)
        write_in_csv(details)  # using function arguments passing
        automatic_email(details)
        pan()
        return redirect('/index.html')
    else:
        return "problem occurred !!!"


if __name__ == '__main__':
    app.run(debug=True)
