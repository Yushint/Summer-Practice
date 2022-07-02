import unittest
from models import UsersModel
from database import DB


class ModelsUnittests(unittest.TestCase):
    def setUp(self):
        self.db = DB()
        self.UserModel = UsersModel(self.db.get_connection())
        self.UserModel.initialize_table()
        self.UserModel.insert("test00", "pass00", "email00@00.00")
        self.UserModel.insert("test01", "pass01", "email01@01.00")
        self.UserModel.insert("test02", "pass02", "email02@02.00")
        self.UserModel.insert("test03", "pass03", "email03@03.00")
                
    #def test_get_user(self):
        #for _id in range(1, 5):
            #with self.subTest(case=_id):
                #data = self.UserModel.get_user(_id)
                #self.assertIsInstance(data, tuple)        
    
    #def test_is_user_exists(self):
        #for _id in range(0, 4):
            #username = "test0" + str(_id)
            #with self.subTest(case=username):
                #data = self.UserModel.is_user_exists(username)
                #self.assertIsInstance(data, tuple)
                
    def test_get_all_users(self):
        data = self.UserModel.get_all_users()
        self.assertIsInstance(data, list)
    
if __name__ == "__main__":
    unittest.main()
