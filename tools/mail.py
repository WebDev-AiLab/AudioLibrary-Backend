from settings import NOTIFICATIONS_EMAIL
from django.core.mail import EmailMessage
# from audiomonsters.celery import app


# @app.task(name='send_html_email')
def send_html_email(receiver_email, sender=NOTIFICATIONS_EMAIL, subject=None, html=None):
    # print('sending...')
    # print('email: ' + receiver_email)
    # print('subject: ' + subject)
    mail = EmailMessage(
        subject=subject,
        body=html,
        from_email=sender,
        to=[receiver_email],
        reply_to=[sender]
    )
    mail.content_subtype = "html"
    try:
        return mail.send()
    except:
        # todo some error handling is needed
        print('failed to send the fucking email')
