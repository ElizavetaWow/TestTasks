from datetime import datetime, timedelta
import unittest
from app import app, db
from app.models import User, Post

class UserModelCase(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    def test_password_hashing(self):
        u = User(username='lisa')
        u.set_password('win')
        self.assertFalse(u.check_password('lose'))
        self.assertTrue(u.check_password('win'))



if __name__ == '__main__':
    unittest.main(verbosity=2)