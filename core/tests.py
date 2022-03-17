from django.contrib.auth.models import User
from django.test import TestCase, Client

from .utils import make_request, are_these_fields_flagged_for
from .views import LoginView, SignupView, ResetPasswordView

INCORRECT_USERNAME_AND_PASSWORD = "Please enter a correct username and password. Note that both fields may be case-sensitive."
REQUIRED_FIELD = "This field is required."
LOGIN_REDIRECT = "/dashboard/"
SIGNUP_SUCCESS = "You are successfully signed up. You can activate your account by confirming your email."
SIGNUP_FAIL = "Failed to signup. Encountered the validation errors below!"
SIGNUP_REDIRECT = "/login/"
EMAIL_INVALID = "Enter a valid email address"
PASSWORDS_NOT_MATCHING = "The passwords do not match"


class LoginViewTestCase(TestCase):
    client = Client()
    route = '/login/'
        
    def test_login_with_missing_password(self):
        data = {'username':'simon'}

        message, errors, redirect, status_code = make_request(self.client, self.route, data)
        err_msg = errors.get('password',None)
        
        self.assertEqual(err_msg, [REQUIRED_FIELD])
        self.assertEqual(status_code, 401)

    def test_login_with_missing_username(self):
  
        data = {'password':'simonsays123'}
        
        message, errors, redirect, status_code = make_request(self.client, self.route, data)
        err_msg = errors.get('username',None)
        
        self.assertEqual(err_msg, [REQUIRED_FIELD])
        self.assertEqual(status_code, 401)

    def test_login_with_incorrect_details(self):

        data = {'username':'simon','password':'simonsays123'}
        
        message, errors, redirect, status_code = make_request(self.client, self.route, data)
        err_msg = errors.get('__all__', None)

        self.assertEqual(err_msg, [INCORRECT_USERNAME_AND_PASSWORD])
        self.assertEqual(status_code, 401)

    def test_login_with_correct_details(self):
        uname = 'simon'
        password = 'simonsays123'
        user = User.objects.create_user(username=uname, password=password)

        data = {'username':uname,'password':password}

        message, errors, redirect, status_code = make_request(self.client, self.route, data)
        
        self.assertEqual(status_code, 200)
        self.assertEqual(redirect, LOGIN_REDIRECT) # Make sure redirect happens after successful login


class SignupViewTestCase(TestCase):
    route = '/signup/'
    client = Client()
    
    def test_signup_with_correct_details(self):
        password = 'simonsays123'
        data = {'username':'simon','email':'simon@123.com',
                'first_name':'Simon','last_name':'Says',
                'password1':password,'password2':password }
        
        message, errors, redirect, status_code = make_request(self.client, self.route, data)
          
        self.assertEqual(message, SIGNUP_SUCCESS)
        self.assertEqual(errors, {})
        self.assertEqual(redirect, SIGNUP_REDIRECT)
        self.assertEqual(status_code, 200)

    def test_signup_validation(self):
        password = 'simonsays123'
    
        message1, errors1, redirect1, status_code1 = make_request(self.client, self.route, {})
        
        # for email validation
        message2, errors2, redirect2, status_code2 = make_request(self.client, self.route,
                                                            {'email': 'wrong email format'})
             
        required_validation_caught = are_these_fields_flagged_for(
            fields=('username', 'email', 'first_name', 
                    'last_name', 'password1', 'password2', ),
            errors=errors1,
            error_msg=REQUIRED_FIELD)

        wrong_email_format_is_caught = are_these_fields_flagged_for(
            fields=('email'),
            errors=errors2,
            error_msg=EMAIL_INVALID
        )
        
        self.assertEqual(message1, SIGNUP_FAIL)
        self.assertEqual(message2, SIGNUP_FAIL)
        self.assertTrue(required_validation_caught)
        self.assertTrue(wrong_email_format_is_caught)
        self.assertNotEqual(redirect1, SIGNUP_REDIRECT) # should not be redirected to dashboard
        self.assertNotEqual(redirect2, SIGNUP_REDIRECT) # should not be redirected to dashboard 
        self.assertEqual(status_code1, 200)
        self.assertEqual(status_code2, 200)

class ResetPasswordViewTestCase(TestCase):
    route = '/reset-password/'
    client = Client()
     
    def test_reset_password(self):
        pass

    def test_reset_password_validation(self):

        data1 = {'step': 1, 'email': 'wrongemail'}
        data2 = {'step': 2, 'password1': '', 'password2':''}
      
        message1, errors1, redirect1, status_code1 = make_request(self.client, self.route, data1)
        message2, errors2, redirect2, status_code2 = make_request(self.client, self.route, data2)

        # test required field validation
        required_validation_caught = are_these_fields_flagged_for(
            fields=('email',),
            errors=errors1,
            error_msg=REQUIRED_FIELD)

        # test if passwords not matching
        password_not_matching_caught = are_these_fields_flagged_for(
            fields=('password1','password2'),
            errors=errors2,
            error_msg=PASSWORDS_NOT_MATCHING)

        self.assertTrue(required_validation_caught)
        self.assertTrue(password_not_matching_caught)