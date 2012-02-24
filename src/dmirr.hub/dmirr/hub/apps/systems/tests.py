"""

$ coverage run manage.py test systems
$ coverage report --include=./apps/systems/views.py
Name                 Stmts   Miss  Cover
----------------------------------------
apps/systems/views      95      2    98%

"""

from django.test import TestCase

class SystemsViewsTestCases(TestCase):
    def setUp(self):
        # a few default objects for testing
        self.client.login(username='admin', password='admin')
        self.client.post('/systems/create/',
                    {
                       'label': 'iuscommunity.org',
                       'user': '1'
                     })
        self.client.post('/projects/create/',
                    {
                       'label': 'test',
                       'user': '1',
                       'display_name': 'test',
                       'admin_group': '',
                       'url': '',
                     })
        self.client.post('/systems/iuscommunity.org/resources/create/',
                    {
                       'project': '1',
                       'path': 'path.com',
                       'protocols': '1',
                       'user': '1',
                       'system': '1'
                     })
        
    def test_list_view(self):
        response = self.client.get('/systems/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('systems' in response.context)
    
    def test_manage_view(self):
        response = self.client.get('/systems/manage/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('systems' in response.context)

    def test_create_view(self):
        response = self.client.get('/systems/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        
    def test_create(self):
        response = self.client.post('/systems/create/',
                    {
                       'label': 'rackspace.com',
                       'user': '1'
                     })
        self.assertRedirects(response, '/systems/rackspace.com/', 302, 200)
        
    def test_update_view(self):
        response = self.client.get('/systems/iuscommunity.org/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        
    def test_update(self):
        response = self.client.post('/systems/iuscommunity.org/update/',
                    {
                       'label': 'rackspace.com',
                       'user': '1',
                     })
        self.assertRedirects(response, '/systems/rackspace.com/', 302, 200)
        
    def test_show_view(self):
        response = self.client.get('/systems/iuscommunity.org/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('system' in response.context)
        
    def test_delete(self):
        response = self.client.get('/systems/iuscommunity.org/delete/')
        self.assertRedirects(response, '/systems/manage/', 302, 200)
        
    def test_create_resource_view(self):
        response = self.client.get('/systems/iuscommunity.org/resources/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('system' in response.context)
        
    def test_create_resource(self):
        response = self.client.post('/systems/iuscommunity.org/resources/create/',
                    {
                       'project': '1',
                       'path': 'newpath.com',
                       'protocols': '1',
                       'user': '1',
                       'system': '1'
                     })
        self.assertRedirects(response, '/systems/iuscommunity.org/', 302, 200)

    def test_update_resource_view(self):
        response = self.client.get('/systems/iuscommunity.org/resources/1/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('resource' in response.context)
        
    def test_update_resource(self):
        response = self.client.post('/systems/iuscommunity.org/resources/1/update/',
                    {
                       'project': '1',
                       'path': 'newpath.org',
                       'protocols': '2',
                       'user': '1',
                       'system': '1'
                     })
        self.assertRedirects(response, '/systems/iuscommunity.org/resources/1/', 302, 200)
        
    def test_show_resource_view(self):
        response = self.client.get('/systems/iuscommunity.org/resources/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('resource' in response.context)
        
    def test_delete_repo_view(self):
        response = self.client.get('/systems/iuscommunity.org/resources/1/delete/')
        self.assertRedirects(response, '/systems/iuscommunity.org/', 302, 200)
