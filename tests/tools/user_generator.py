import random
import string

class UserGenerator:
    @staticmethod
    def generate_random_user_data():
        """
        Generate random data for a new user registration.
        """
        display_name = ''.join(random.choices(string.ascii_letters, k=8))
        handle_name = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return {
            "display_name": display_name,
            "handle_name": handle_name,
            "password": password
        }
