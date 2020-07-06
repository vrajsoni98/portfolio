from flask import Flask, render_template, url_for, request, redirect
import csv
from datetime import date
import smtplib
import config

app = Flask(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

# def write_to_file(data):
#     with open('database.txt', mode='a') as database:
#         email = data["email"]
#         subject = data["subject"]
#         message = data["message"]
#         file = database.write(f'\n{email},{subject},{message}')

def write_to_csv(data):
    today = date.today()
    with open('database.csv', newline='', mode='a') as database2:
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        day = today.strftime("%B %d, %Y")
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message,day])

def send_email(data):
    try:
        subject = data["subject"]
        message = data["email"]+"\n"+data["message"]
        c_subject="This is auto generated email"
        c_message="Hello !! I am Vraj Soni.Thanks for contacting me. I will get in touch with you shortly"
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(config.EMAIL_ADDRESS, config.PASSWORD)
        client_message = 'Subject: {}\n\n{}'.format(c_subject,c_message)
        vraj_message = 'Subject: {}\n\n{}'.format(subject,message)
        server.sendmail(config.EMAIL_ADDRESS, data["email"], client_message)
        server.sendmail(config.EMAIL_ADDRESS, config.EMAIL_ADDRESS1, vraj_message)
        server.quit()
        print("Success: Email sent!")
    except:
        print("Email failed to send.")

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
      try:
        data = request.form.to_dict()
        write_to_csv(data)
        send_email(data)
        return redirect('/thankyou.html')
      except:
        return 'did not save to database'
    else:
      return 'something went wrong. Try again!'

if __name__ == '__main__':
    app.run()
