import unittest
from app.welcome_window import is_valid_email

class TestIsValidEmail(unittest.TestCase):

    def test_valid_emails(self):
        # Test valid email addresses
        valid_emails = [
            "user@example.com",
            "first.last@example.com",
            "user123@example.com",
            "user+test@example.com",
            "user@example-domain.com",
            "user@example.co.uk",
            "user123@example.domain.com"
        ]
        for email in valid_emails:
            with self.subTest(email=email):
                self.assertTrue(is_valid_email(email))

    def test_invalid_emails(self):
        # Test invalid email addresses
        invalid_emails = [
            "user@example",
            "user.example.com",
            "user@.com",
            "user@domain",
            "user@.123",
            "@example.com",
            "user@.com.",
            "user@.com.."
        ]
        for email in invalid_emails:
            with self.subTest(email=email):
                self.assertFalse(is_valid_email(email))

if __name__ == '__main__':
    unittest.main()