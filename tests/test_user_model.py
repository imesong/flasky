import unittest
from app.models import User, Role, Permissions, AnonymousUser


class UserModelTestCase(unittest.TestCase):
    def test_password_setter(self):
        u = User(password='imesong')
        self.assertTrue(u.password_hash is not None)

    def test_set_not_password_getter(self):
        u = User(password='imesong')
        with self.assertRaises(AttributeError):u.password

    def test_verify(self):
        u = User(password='imesong')
        self.assertTrue(u.verify_password('imesong'))
        self.assertFalse(u.verify_password('qiangge'))

    def test_password_salt_random(self):
        u = User(password='imesong')
        u2 = User(password='qiangge')
        self.assertTrue(u.password_hash != u2.password_hash)

    def test_roles_permissions(self):
        Role.insert_roles()
        u = User(email='abc@126.com', password='cat')
        self.assertTrue(u.can(Permissions.WRITE_ARTICLES))
        self.assertFalse(u.can(Permissions.MODIFY_COMMENTS))

    def test_anonymoususer(self):
        u = AnonymousUser()
        self.assertFalse(u.can(Permissions.FOLLOW))