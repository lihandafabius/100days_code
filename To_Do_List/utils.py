import smtplib
from flask import current_app

def send_reminder_email(user, task):
    try:
        with smtplib.SMTP(current_app.config['MAIL_SERVER'], current_app.config['MAIL_PORT']) as connection:
            connection.starttls()
            connection.login(
                user=current_app.config['MAIL_USERNAME'],
                password=current_app.config['MAIL_PASSWORD']
            )
            message = f"Subject: Task Due Today\n\nDear {user.username},\n\nThis is a reminder that your task '{task.task}' is due today."
            connection.sendmail(
                from_addr=current_app.config['MAIL_USERNAME'],
                to_addrs=user.email,
                msg=message
            )
    except Exception as e:
        current_app.logger.error(f"Failed to send email: {e}")