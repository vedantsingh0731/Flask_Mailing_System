from flask import Flask, request, jsonify
from flask_mail import Mail, Message
import logging
import os
from dotenv import load_dotenv

# Logger class
class Logger:
    def __init__(self, name="FlaskApp"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self._set_handler()

    def _set_handler(self):
        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        # Define the format for logs
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self):
        return self.logger


# Creating the logger
log = Logger().get_logger()

app = Flask(__name__)

# Configure Flask-Mail with Oracle Email Delivery SMTP settings
# Configure Flask-Mail using environment variables
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))  # Convert to int
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'  # Convert to boolean
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'  # Convert to boolean
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_ATTACHMENT_PATH'] = os.getenv('MAIL_ATTACHMENT_PATH')


# Initialize Flask-Mail
mail = Mail(app)


def send_email():
    try:
        log.info("Processing email request...")

        # Recipients, subject, body
        recipient = ["vedantsinghintern@gmail.com", "mauryaaankit2112@gmail.com"]
        subject = "this is test subject"
        body = "this is test body"

        # Create the email message
        msg = Message(subject=subject, recipients=recipient, body=body)

        # Attach the file to the email
        log.info("Attaching file to email...")
        with app.open_resource("attachments/Ankit_resume.pdf") as fp:
            msg.attach(
                filename="Ankit_resume.pdf",
                content_type="application/pdf",
                data=fp.read()
            )

        # Send the email
        mail.send(msg)
        log.info("Email sent successfully!")

        return jsonify({"message": "Email sent successfully!"}), 200
    except Exception as e:
        log.error(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 400

# Adding the Route
@app.route('/send-email', methods=['POST'])
def send_email_endpoint():
    return send_email()



if __name__ == '__main__':
    app.run(debug=True)
