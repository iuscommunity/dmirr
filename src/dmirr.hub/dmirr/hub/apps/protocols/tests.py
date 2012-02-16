"""

$ coverage run manage.py test protocols
$ coverage report --include=./apps/protocols/views.py
Name                   Stmts   Miss  Cover
------------------------------------------
apps/protocols/views      49      0   100%

"""

from django.test import TestCase

class ProtocolsViewsTestCases(TestCase):
    def setUp(self):
        # a few default objects for testing
        self.client.login(username='admin', password='admin')
        
    def test_list_view(self):
        response = self.client.get('/protocols/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('protocols' in response.context)

    def test_manage_view(self):
        response = self.client.get('/protocols/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('protocols' in response.context)

    def test_create_view(self):
        response = self.client.get('/protocols/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
    
    def test_create(self):
        response = self.client.post('/protocols/create/',
                    {
                       'label': 'http2',
                       'port': '8080'
                     })
        self.assertRedirects(response, '/protocols/manage/', 302, 200)
        
    def test_update_view(self):
        response = self.client.get('/protocols/http/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('protocol' in response.context)
    
    def test_update(self):
        response = self.client.post('/protocols/http/update/',
                    {
                       'label': 'http2',
                       'port': '8080'
                     })
        self.assertRedirects(response, '/protocols/manage/', 302, 200)
        
    def test_show_view(self):
        response = self.client.get('/protocols/http/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('protocol' in response.context)
        
    def test_delete(self):
        response = self.client.get('/protocols/http/delete/')
        self.assertRedirects(response, '/protocols/manage/', 302, 200)
