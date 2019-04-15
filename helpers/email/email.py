from .email_setup import SendEmail
from config import Config
from flask import render_template
from api.room.models import Room as RoomModel


class EmailNotification:
    """
    Send email notifications
    """
    def send_email_notification(
        self, **kwargs
    ):
        # general send email notifications
        recipients = [kwargs.get('email')]

        email = SendEmail(
            kwargs.get('subject'), recipients,
            render_template(
                kwargs.get('template'),
                location_name=kwargs.get('location_name'),
                user_name=kwargs.get('user_name'),
                room_name=kwargs.get('room_name'),
                event_title=kwargs.get('event_title'),
                event_reject_reason=kwargs.get('event_reject_reason')
            ))

        return email.send()

    def email_invite(self, email, admin):
        # send email on user registration
        email = SendEmail(
            "Invitation to join Converge", [email],
            render_template('invite.html', name=admin,
                            domain=Config.DOMAIN_NAME)
            )

        return email.send()

    def event_cancellation_notification(
        self, organizer_email, room_id, event_title, event_reject_reason
    ):
        # send email on event cancellation
        room = RoomModel.query.filter_by(id=room_id).first()
        room_name = room.name
        subject = 'Your room reservation was rejected'
        template = 'event_cancellation.html'
        return EmailNotification.send_email_notification(
            self, email=organizer_email, subject=subject, template=template,
            room_name=room_name, event_title=event_title,
            event_reject_reason=event_reject_reason
        )


notification = EmailNotification()
