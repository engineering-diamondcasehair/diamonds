#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask_mail import Mail
from flask_mail import Message

RECIPIENTS = ['mailbox@diamondcasehair.com',
              'jonathan.k.sulllivan@gmail.com']


def setup_mail(app):
    return Mail(app)


def send_message_to_dc(
    sender,
    subject,
    message,
    app,
    mail,
    ):
    message = Message(body=message, sender=sender, recipients=RECIPIENTS,
                      reply_to='no-reply@diamondcase.com')
    message.subject = subject
    mail.send(message)
    log_message(message=message, app=app)


def log_message(message, app):
    log_msg = f"""
        Message(
            'subject': {message.subject},
            'recipients': {message.recipients},
            'body': {message.body},
            'html': {message.html},
            'sender': {message.sender},
            'cc': {message.cc},
            'bcc': {message.bcc},
            'attachments': {message.attachments},
            'reply_to': {message.reply_to},
            'date': {message.date},
            'charset': {message.charset},
            'extra_headers': {message.extra_headers},
            'mail_options': {message.mail_options},
            'rcpt_options': {message.rcpt_options})"""
    app.logger.debug(log_msg)