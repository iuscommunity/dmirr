"""
$ coverage run manage.py test base
$ coverage report --include=./apps/base/views.py
Name    Stmts   Miss  Cover
---------------------------

"""

from django.test import TestCase

class BaseViewsTestCases(TestCase):
    def setUp(self):
        # a few default objects for testing
        self.client.login(username='admin', password='admin')
        
    #def test_index_view(self):
    #    response = self.client.get('/base/')
    #    self.assertEqual(response.status_code, 200)
    #    self.assertTrue('data' in response.context)
