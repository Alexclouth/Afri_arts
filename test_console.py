import unittest
from console import AfriArts
from io import StringIO
import sys
from unittest.mock import patch
from models import storage
from models.user import User

class TestAfriArts(unittest.TestCase):
    """Test suite for the HBNBCommand class"""

    def setUp(self):
        """Set up test environment"""
        self.cli = AfriArts()
        storage._FileStorage__objects.clear()  # Clear storage between tests


    def tearDown(self):
        """Clean up test environment"""
        storage._FileStorage__objects.clear()
        storage._FileStorage__objects.clear()

    def test_quit(self):
        """Test quit command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.cli.onecmd("quit"))

    def test_emptyline(self):
        """Test emptyline command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("")
            self.assertEqual(f.getvalue(), "")

    def test_create(self):
        """Test create command"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd('create User')
            user_id = f.getvalue().strip()
            self.assertIn(f"User.{user_id}", storage.all())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("create NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_show(self):
        """Test show command"""
        user = User()
        user.save()

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"show User {user.id}")
            self.assertIn(user.id, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("show User NonExistentID")
            self.assertEqual(f.getvalue().strip(), "** no instance found **")
        
    def test_destroy(self):
        """Test destroy command"""
        user = User()
        user.save()
    
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f'User.destroy("{user.id}")')
            self.assertNotIn(f"User.{user.id}", storage.all())
    
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("destroy")
            self.assertEqual(f.getvalue().strip(), "** class name missing **")
    
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("destroy NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")
    
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd('User.destroy("NonExistentID")')
            self.assertEqual(f.getvalue().strip(), "** no instance found **")

    def test_all(self):
        """Test all command"""
        user = User()
        user.save()
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all User")
            self.assertIn(f"[User] ({user.id})", f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("all NonExistentClass")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

    def test_update_with_single_attribute(self):
        """Test update command with a single attribute"""
        user = User()
        user.save()
    
        # Perform the update
        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f'User.update("{user.id}", "first_name", "John")')
    
        # Fetch the updated user from storage
        updated_user = storage.all().get(f"User.{user.id}")
    
        # Debugging output
        if updated_user is None:
            self.fail("Updated user not found in storage.")
        
        # Check if the first_name was updated correctly
        self.assertEqual(updated_user.first_name, "John")
        print(f"Updated first_name: {updated_user.first_name}")

            

    def test_update_with_dict(self):
        """Test update command with a dictionary of attributes"""
        user = User()
        user.save()

        update_dict = {'first_name': "John", "age": 89}


    def test_count(self):
        """Test count command"""
        user1 = User()
        user1.save()
        user2 = User()
        user2.save()

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("count User")
            self.assertEqual(int(f.getvalue().strip()), 2)

    def test_default(self):
        """Test default method"""
        user1 = User()
        user1.save()
        user2 = User()
        user2.save()

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("User.count()")
            self.assertEqual(int(f.getvalue().strip()), 2)

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"User.show({user1.id})")
            self.assertIn(user1.id, f.getvalue())

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f'User.update("{user1.id}", "first_name", "John")')
            self.assertEqual(storage.all()[f"User.{user1.id}"].first_name, 'John')

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd(f"User.update({user2.id}, {{'last_name': 'Doe', 'age': 30}})")
            updated_user = storage.all()[f"User.{user2.id}"]
            self.assertEqual(updated_user.last_name, "Doe")
            self.assertEqual(updated_user.age, 30)

        with patch('sys.stdout', new=StringIO()) as f:
            self.cli.onecmd("NonExistentClass.all()")
            self.assertEqual(f.getvalue().strip(), "** class doesn't exist **")

if __name__ == '__main__':
    unittest.main()

