import unittest
from main import validate_result
from main import natural_keys

class test_application(unittest.TestCase):

    def test_class_creation(self):
        self.assertEqual(validate_result("hgf"),None)
        self.assertEqual(validate_result("1 а"),None)
        self.assertEqual(validate_result("1 f"),None)
        self.assertEqual(validate_result(""),None)

        self.assertIsNotNone(validate_result("1 А"))
        self.assertIsNotNone(validate_result("10 А"))
       
    def test_class_sorting(self):
        class_list = []
        class_list_success = ["3 Б.pic","5 А.pic","10 А.pic","10 Г.pic"]
        a1 = "5 А.pic"
        b2 = "3 Б.pic"
        с3 = "10 Г.pic"
        d4 = "10 А.pic"
        class_list.append(a1)
        class_list.append(b2)
        class_list.append(с3)
        class_list.append(d4)
        class_list.sort(key=natural_keys)
        self.assertEquals(class_list,class_list_success)


    