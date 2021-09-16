import unittest
from DiamondCaseWeb import create_app
from DiamondCaseWeb.util import dc_mail

class MailTests(unittest.TestCase):
    def setUp(self):
      self.app = create_app()
      self.app.config.from_object('DiamondCaseWeb.config.TestingConfig')
      self.context = self.app.app_context()
      self.app.config.from_object('DiamondCaseWeb.config.TestingConfig')
      self.context.push()
      self.mail = dc_mail.setup_mail(self.app)

    def tearDown(self):
      self.context.pop()

    def test_mail(self):
      with self.app.app_context():
        with self.mail.record_messages() as outbox:
          dc_mail.send_message_to_dc(
            sender='testing@testing.com',
            subject='testing',
            message='message',
            app=self.app,
            mail=self.mail)
          self.assertEqual(len(outbox), 1)
          self.assertEqual(outbox[0].subject, "testing")
          self.assertEqual(outbox[0].body, "message")

if __name__ == '__main__':
    unittest.main()