import firebase_admin
from firebase_admin import credentials, messaging
from helpers.converter import clean_msg_for_notif

cred = credentials.Certificate("configs/gudangku-94edc-firebase-adminsdk-we9nr-408864292c.json")
firebase_admin.initialize_app(cred)

def send_fcm_notif(token, title, body, obj=None):
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=clean_msg_for_notif(body),
        ),
        data=obj,
        token=token,
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)

