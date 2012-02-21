"""
$ coverage run manage.py test archs
$ coverage report --include=./apps/archs/views.py
Name               Stmts   Miss  Cover
--------------------------------------
apps/archs/views      49      3    94%

"""

from django.test import TestCase

class ArchsViewsTestCases(TestCase):
    def setUp(self):
        # a few default objects for testing
        self.client.login(username='admin', password='admin')
    
    def test_index(self):
        response = self.client.get('/archs/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('archs' in response.context)
        
    def test_manage(self):
        response = self.client.get('/archs/manage/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('archs' in response.context)

    def test_create_arch_index(self):
        response = self.client.get('/archs/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        
    def test_create_arch(self):
        response = self.client.post('/archs/create/', {'label': 'i586'})
        self.assertRedirects(response, '/archs/manage/', 302, 200)

    def test_update_404(self):
        response = self.client.get('/archs/invalidArch/update/')
        self.assertEqual(response.status_code, 404)
        
    def test_update_index(self):
        response = self.client.get('/archs/i386/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        
    def test_update(self):
        response = self.client.post('/archs/i386/update/', {'label': 'i586'})
        self.assertRedirects(response, '/archs/manage/', 302, 200)

    def test_delete(self):
        response = self.client.get('/archs/i386/delete')
        self.assertRedirects(response, '/archs/i386/delete/', 301, 302)
        
