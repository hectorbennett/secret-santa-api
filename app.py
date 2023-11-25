"""
send POST request with

{
	"santas": [
		{
			"santa": "human 1",
			"email": "human1@email.com"
		},
		{
			"santa": "human 2",
			"email": "human2@email.com"
		},
		{
			"santa": "human 3",
			"email": "human3@email.com"
		},
		{
			"santa": "human 4",
			"email": "human4@email.com"
		},
		{
			"santa": "human 5",
			"email": "human5@email.com"
		},
		{
			"santa": "human 6",
			"email": "human6@email.com"
		}
	],
	"invalid_pairs": [
		[
			"human 1",
			"human 2",
			"human 4"
		],
		[
			"human 4",
			"human 5"
		]
	],
	"message": "Dear {santa}, buy something for {giftee}",
	"subject": "Hi {santa}",
    "test": true
}

"""
import os
from flask import Flask, request, jsonify
from flask_mail import Mail, Message
from dotenv import load_dotenv

load_dotenv()

from generate_assignments import generate_assignments

app = Flask(__name__)


app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = True if os.getenv('MAIL_USE_TLS') == 'true' else False
app.config['MAIL_USE_SSL'] = True if os.getenv('MAIL_USE_SSL') == 'true' else False
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

mail = Mail(app)

def send_emails(sender, emails):
    with mail.connect() as conn:
        for email in emails:
            msg = Message(
                sender=sender,
                recipients=email['recipients'],
                subject=email['subject'],
                body=email['body'],
                bcc=email.get('bcc'),
            )
            conn.send(msg)

tags = ['santa', 'giftee', 'email']

def send_santa_emails(santas, bcc='', subject_template='', message_template=''):
    emails = []
    for santa in santas:
        emails.append({
            'recipients': [santa['email']],
            'bcc': [bcc] if bcc else None,
            'subject': replace_merge_tags(subject_template, santa),
            'body': replace_merge_tags(message_template, santa),
        })
    send_emails(('SantaBot 3000', 'secret-santa@hectorbennett.com'), emails)

def replace_merge_tags(template, data):
    text = template
    for tag in tags:
        if data.get(tag):
            text = text.replace(f'{{{tag}}}', data[tag])
    return text


@app.route("/", methods=['GET', 'POST'])
def main():
    if request.method == 'POST':
        return post(request)
    return "<p>Send a POST request to this url to send emails</p>"

def post(request):
    data = request.get_json()

    if not data:
        return "No json payload supplied"

    santas = data.get('santas')
    invalid_pairs = data.get('invalid_pairs')
    message_template = data.get('message')
    subject_template = data.get('subject')

    if not santas:
        return "No 'santas' array supplied in json payload"
    if not message_template:
        return "No 'message' string supplied in json payload"
    if not subject_template:
        return "No 'subject' string supplied in json payload"
    if '{santa}' not in message_template:
        return "{santa} merge tag not found in 'message' string"
    if '{giftee}' not in message_template:
        return "{giftee} merge tag not found in 'message' string"

    santa_names = [s['santa'] for s in santas]
    duplicates = set([n for n in santa_names if santa_names.count(n) > 1])
    if duplicates:
        return 'Duplicate names found: {}'.format(', '.join(duplicates))
    
    assignments = generate_assignments(santas, invalid_pairs=invalid_pairs)

    if not assignments:
        return 'Could not find a valid assignment'

    if not data.get('test'):
        send_santa_emails(assignments, bcc=data.get('bcc'), subject_template=subject_template, message_template=message_template)

    return jsonify(assignments)
