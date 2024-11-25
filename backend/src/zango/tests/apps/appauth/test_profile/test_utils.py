from django.test import TestCase
from django.conf import settings
from zango.api.app_auth.profile.v1.utils import PasswordValidationMixin

class TestPasswordValidation(TestCase):
    def setUp(self):
        self.validator = PasswordValidationMixin()
        self.valid_password = "TestPass123!@#"
    
    def test_password_matching(self):
        # Test matching passwords
        result = self.validator.is_password_matching("Test123!", "Test123!")
        self.assertTrue(result["validation"])
        self.assertIsNone(result["msg"])
        
        # Test non-matching passwords
        result = self.validator.is_password_matching("Test123!", "Test1234!")
        self.assertFalse(result["validation"])
        self.assertEqual(result["msg"], "The two passwords didn't match!")

    def test_password_length(self):
        # Test valid length
        result = self.validator.check_password_length(self.valid_password)
        self.assertTrue(result["validation"])
        self.assertIsNone(result["msg"])
        
        # Test invalid length
        short_password = "Ab1!"
        result = self.validator.check_password_length(short_password)
        self.assertFalse(result["validation"])
        self.assertIn(str(settings.PASSWORD_MIN_LENGTH), result["msg"])

    def test_first_character_alpha(self):
        # Test valid first character
        result = self.validator.is_first_alpha(self.valid_password)
        self.assertTrue(result["validation"])
        self.assertIsNone(result["msg"])
        
        # Test invalid first character
        result = self.validator.is_first_alpha("123Test!")
        self.assertFalse(result["validation"])
        self.assertEqual(result["msg"], "The first letter of your password must be an alphabet!")

    def test_uppercase_character(self):
        # Test with uppercase
        result = self.validator.check_uppercase_char(self.valid_password)
        self.assertTrue(result["validation"])
        self.assertIsNone(result["msg"])
        
        # Test without uppercase
        result = self.validator.check_uppercase_char("test123!")
        self.assertFalse(result["validation"])
        self.assertEqual(result["msg"], "The new password must contain at least one upper case character")

    def test_lowercase_character(self):
        # Test with lowercase
        result = self.validator.check_lowercase_char(self.valid_password)
        self.assertTrue(result["validation"])
        self.assertIsNone(result["msg"])
        
        # Test without lowercase
        result = self.validator.check_lowercase_char("TEST123!")
        self.assertFalse(result["validation"])
        self.assertEqual(result["msg"], "The new password must contain at least one lower case character")

    def test_special_character(self):
        # Test with special character and number
        result = self.validator.check_special_character(self.valid_password)
        self.assertTrue(result["validation"])
        self.assertEqual(result["msg"], "")
        
        # Test without special character
        result = self.validator.check_special_character("TestPass123")
        self.assertFalse(result["validation"])
        
        # Test without number
        result = self.validator.check_special_character("TestPass!@#")
        self.assertFalse(result["validation"])

    def test_run_all_validations(self):
        # Create a mock user
        class MockUser:
            def check_password_validity(self, password):
                return False
            @property
            def email(self):
                return "test@example.com"
            
        user = MockUser()
        
        # Test valid password
        result = self.validator.run_all_validations(
            user=user,
            password=self.valid_password,
            repeat_password=self.valid_password,
            old_password=None
        )
        self.assertTrue(result["validation"])
        self.assertEqual(result["msg"], "Password validations passed")