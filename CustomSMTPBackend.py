from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
import smtplib

class CustomSMTPBackend(SMTPBackend):
    def __init__(self, *args, **kwargs):
        self.keyfile = kwargs.pop('keyfile', None)
        self.certfile = kwargs.pop('certfile', None)
        super().__init__(*args, **kwargs)

    def open(self):
        self.connection = smtplib.SMTP(self.host, self.port)
        if self.use_tls:
            self.connection.starttls()
        if self.keyfile and self.certfile:
            self.connection.sock = smtplib.SMTP_SSL(
                self.host, self.port,
                keyfile=self.keyfile,
                certfile=self.certfile
            )
