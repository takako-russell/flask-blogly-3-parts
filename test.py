
from unittest import TestCase
from app import app
from models import db, User


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True



class UserRouteTests(TestCase):

    def setUp(self):
        with app.test_request_context():
        
            db.drop_all()
            db.create_all()

            user = User(first_name = 'Wabi', last_name = 'Russell', image_url='')
            db.session.add(user)
            db.session.commit()

            self.client = app.test_client()
        

    def tearDown(self):
        db.session.rollback()


    def test_list_users(self):
        with self.client:
            res = self.client.get('/users')
            self.assertIn(b'Wabi',res.data)

            
    def test_details(self):
        with self.client:
            res = self.client.get("/users/1")
            self.assertIn(b"Wabi",res.data)

     
    def test_adduser(self):
        data = {
              'firstname':'Hello',
              'lastname': 'Kitty',
              'imageURL':''
        }

        res = self.client.post("/users/new",data=data)
        user = User.query.filter_by(first_name = 'Hello', last_name='Kitty').first()
        self.assertIsNotNone(user)
        self.assertEqual(res.status_code,302)
        

    def test_delete(self):

        res = self.client.post("/users/1/delete")
        user = User.query.get(1)

        self.assertIsNone(user)

    
    

    
       