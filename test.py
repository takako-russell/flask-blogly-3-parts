
from unittest import TestCase
from app import app
from models import db, User,Post


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///user_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True



class UserRouteTests(TestCase):

    def setUp(self):
        with app.test_request_context():
        
            db.drop_all()
            db.create_all()

            user = User(first_name = 'Wabi', last_name = 'Russell', image_url='')
            # post = Post(title='trip',content='it was amazing')
            db.session.add(user)
            # db.session.add(post)

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


    def test_newpost(self):

        data = {
            "new_title":"omg",
            "new_content":"what a day"
        }

        res = self.client.post("/users/1/posts/new", data=data,follow_redirects=True)

        self.assertEqual(res.status_code, 200)
        post = Post.query.filter_by(title='omg').first()

        self.assertEqual(post.content,'what a day')


    def test_edit_post(self):
        user_id=1
        post_id=1

        post = Post(title='trip',content='it was amazing')
        db.session.add(post) 
        db.session.commit()


        res = self.client.get(f"/users/{user_id}/posts/{post_id}/edit", follow_redirects=True)

        self.assertEqual(res.status_code,200)



    def test_editpost(self):
        user_id=1
        post_id=1

        post = Post(title='trip',content='it was amazing')
        id = db.session.add(post) 
        db.session.commit()
       
        data ={"edit-title":"yesterday", "edit-content":"it was rainy"}

        res = self.client.post(f"/users/{user_id}/posts/{post_id}/edit", data=data, follow_redirects=True)
                            #    data=data,follow_redirects=True)
        self.assertEqual(res.status_code,200)

        post = Post.query.filter_by(title="yesterday").first()

        self.assertEqual(post.content,'it was rainy')





    
    

    
       