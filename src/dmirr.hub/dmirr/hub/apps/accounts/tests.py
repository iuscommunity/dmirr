"""

$ coverage run manage.py test accounts
$ coverage report --include=./apps/accounts/views.py
Name                  Stmts   Miss  Cover
-----------------------------------------
apps/accounts/views      92      7    92%

"""

from django.test import TestCase

class AccountViewsTestCases(TestCase):
    def setUp(self):
        # a few default objects for testing
        self.client.login(username='admin', password='admin')
        self.client.post('/account/groups/create/', {'name': 'test'})
        self.client.post('/account/groups/1/add/', {'user': 1})
    
    def test_api_access(self):
        response = self.client.get('/account/admin/api_access/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('user' in response.context)
        self.assertTrue('profile' in response.context)
        
    def test_reset_api_key(self):
        response = self.client.get('/account/admin/reset_api_key/')
        self.assertRedirects(response, '/account/admin/api_access/', 302, 200)
        response = self.client.get('/account/admin/api_access/')
        self.assertTrue(response.context['user'].api_key.key)

    def test_list_groups(self):
        response = self.client.get('/account/groups/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('groups' in response.context)

    def test_manage_groups(self):
        response = self.client.get('/account/groups/manage/')
        self.assertEqual(response.status_code, 200)

    def test_create_group_index(self):
        response = self.client.get('/account/groups/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        
    def test_create_group(self):
        response = self.client.post('/account/groups/create/', {'name': 'g0'})
        self.assertRedirects(response, '/groups/2/', 302, 200)
        
    def test_delete_group(self):
        response = self.client.get('/account/groups/1/delete/')
        self.assertRedirects(response, '/account/groups/manage/', 302, 200)
        
    def test_update_group_index(self):
        response = self.client.get('/account/groups/1/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('group' in response.context)
        
    def test_update_group(self):
        response = self.client.post('/account/groups/1/update/', {'name': 'g1'})
        self.assertRedirects(response, '/groups/1/', 302, 200)
        
    def test_show_group(self):
        response = self.client.get('/groups/1/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('group' in response.context)
        
    def test_add_user_to_group(self):
        response = self.client.post('/account/groups/1/add/',
                                    {'user': 2})
        self.assertRedirects(response, '/groups/1/', 302, 200)
        
    def test_remove_user_to_group(self):
        response = self.client.get('/account/groups/1/remove/?user=admin')
        self.assertRedirects(response, '/groups/1/', 302, 200)
        
        
