from concurrent.futures import ThreadPoolExecutor

from django.conf import settings
from django.core.mail import EmailMultiAlternatives


class EmailMulti(EmailMultiAlternatives):

    def __init__(self, subject, text_body, recipient_list, html_body=None, callback_fn=None, bcc=None, attachments=None, cc=None, reply_to=None):

        super().__init__(subject=subject, body=text_body, to=recipient_list, from_email=settings.EMAIL_SENDER, bcc=bcc, attachments=attachments, cc=cc, reply_to=reply_to)

        if html_body:
            self.attach_alternative(html_body, "text/html")
        self.callback_fn = callback_fn

    def send_bg(self, callback_fn=None, fail_silently=False):
        """Send email in another thread"""
        callback_fn = callback_fn or self.callback_fn

        with ThreadPoolExecutor() as executor:
            future = executor.submit(self.send, fail_silently)

            if callback_fn:
                future.add_done_callback(callback_fn)

        return future
