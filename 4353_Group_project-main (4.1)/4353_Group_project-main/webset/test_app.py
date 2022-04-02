import unittest
import coverage
from app import app

#to run the code coverage test excute commend below:
#   coverage run test_app.py
#   coverage report -m
#   coverage html

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()

    def tearDown(self):
        self.ctx.pop()

    def test_home(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert "<title>QuotEZ</title>" in response.get_data(as_text=True)


    def test_signup(self):
        response = self.client.get("/signup")
        assert response.status_code == 200
        assert "<title>Registration</title>" in response.get_data(as_text=True)
        
    def test_signup2(self):
        username = "1234"
        password = "Abc12345"
        response = self.client.post("/registration", data={"username": username, "password": password, "password_confirm": password})
        assert response.status_code == 400
    
    def test_signup3(self):
        username = "1234"
        password = "Abc12345"
        response = self.client.post("/registration", data={"name": username, "password": password, "password_confirm": password})
        assert response.status_code == 302
        assert "<title>Redirecting...</title>" in response.get_data(as_text=True)
        
    def test_signup4(self):
        username = "1234"
        password = "Abc12345"
        response = self.client.post("/registration", data={"name": username, "password": password, "password_confirm": ""})
        assert response.status_code == 200
        print(response.get_data(as_text=True))
        assert "password dost not match" ==  response.get_data(as_text=True)
        
    def test_signup4(self):
        username = "1234"
        password = "Abc1234"
        response = self.client.post("/registration", data={"name": username, "password": password, "password_confirm": password})
        assert response.status_code == 200
        assert "name is exists" ==  response.get_data(as_text=True)
        
    def test_signup5(self):
        username = "12345"
        password = "Abc1234"
        response = self.client.post("/registration", data={"name": username, "password": password, "password_confirm": password})
        assert response.status_code == 200
        assert "password should be 8-64 characters" ==  response.get_data(as_text=True)
    
    def test_signup6(self):
        username = "123459"
        password = "212341235413451345"
        response = self.client.post("/registration", data={"name": username, "password": password, "password_confirm": password})
        assert response.status_code == 200
        assert "password must include a capital letter and a number" ==  response.get_data(as_text=True)
    
    def test_login(self):
        username = "123459"
        password = "212341235413451345"
        response = self.client.get("/login")
        assert response.status_code == 200
        assert " <title>Login</title>" in  response.get_data(as_text=True)
        
    def test_login2(self):
        username = "test"
        password = "Abc12345"
        response = self.client.post("/login", data={"username": username, 'psw': password})
        assert response.status_code == 302
    
    def test_login3(self):
        username = "test"
        password = "Abc123456"
        response = self.client.post("/login", data={"username": username, 'psw': password})
        assert response.status_code == 200
        assert "username and password dost not match" ==  response.get_data(as_text=True)
        
    def test_login4(self):
        username = ""
        password = "Abc123456"
        response = self.client.post("/login", data={"username": username, 'psw': password})
        assert response.status_code == 200
        assert "please enter username" ==  response.get_data(as_text=True)
    
    def test_login5(self):
        username = "1234"
        password = ""
        response = self.client.post("/login", data={"username": username, 'psw': password})
        assert response.status_code == 200
        assert "please enter password" ==  response.get_data(as_text=True)
        
    def test_login6(self):
        username = "qawerqwe"
        password = "asdfasdf"
        response = self.client.post("/login", data={"username": username, 'psw': password})
        assert response.status_code == 200
        assert "username dost not exist" ==  response.get_data(as_text=True)
        
    def test_profile(self):
        response = self.client.get("/profile")
        assert response.status_code == 302
    
    def test_profile1(self):
        with self.client.session_transaction() as sess:
            sess['user'] = 'test'

        response = self.client.get("/profile")
        assert response.status_code == 200
        assert "<title>User Profile</title>" in  response.get_data(as_text=True)
        
    def test_profile2(self):
        with self.client.session_transaction() as sess:
            sess['user'] = 'test'

        profile = {'name': '', 'address1': '', 'address2': '', 'city': '', 'zipcode': '', 'state': ''}
        response = self.client.post("/profile", data=profile)
        assert response.status_code == 200
        assert  "Zipcode is too short" in  response.get_data(as_text=True)
        
    def test_profile3(self):
        with self.client.session_transaction() as sess:
            sess['user'] = 'test'

        profile = {'name': '1234', 'address1': '1', 'address2': '2', 'city': 'city', 'zipcode': '12341234', 'state': 'al'}
        response = self.client.post("/profile", data=profile)
        assert response.status_code == 302
        
    
    def test_quote(self):
        response = self.client.get("/quote")
        assert response.status_code == 302
        
    def test_quote1(self):
        with self.client.session_transaction() as sess:
            sess['user'] = 'test'

        response = self.client.get("/quote")
        assert response.status_code == 200
        
    def test_quote_history(self):
        with self.client.session_transaction() as sess:
            sess['user'] = 'test'

        response = self.client.get("/quote_history")
        assert response.status_code == 200
        
    def test_quote_history1(self):
        response = self.client.get("/quote_history")
        assert response.status_code == 302


if __name__ == "__main__":
    unittest.main()

