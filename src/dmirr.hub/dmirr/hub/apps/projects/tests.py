"""
$ coverage run manage.py test projects
$ coverage report --include=./apps/projects/views.py
Name                  Stmts   Miss  Cover
-----------------------------------------
apps/projects/views     103      4    96%

"""

from django.test import TestCase

class ProjectsViewsTestCases(TestCase):
    def setUp(self):
        # a few default objects for testing
        self.client.login(username='admin', password='admin')
        self.client.post('/projects/create/',
                    {
                       'label': 'test',
                       'user': '1',
                       'display_name': 'test',
                       'admin_group': '',
                       'url': '',
                     })
        self.client.post('/projects/test/repos/create/',
                    {
                        'label': 'test_repo',
                        'user': '1',
                        'display_name': 'test repo',
                        'path': 'test repo',
                        'archs': '1',
                        'project': '1'
                     })

    def test_list_view(self):
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('projects' in response.context)
        
    def test_manage_view(self):
        response = self.client.get('/projects/manage/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('projects' in response.context)
        
    def test_create_view(self):
        response = self.client.get('/projects/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        
    def test_create(self):
        response = self.client.post('/projects/create/',
                    {
                       'label': 'testing',
                       'user': '1',
                       'display_name': 'testing',
                       'admin_group': '',
                       'url': '',
                     })
        self.assertRedirects(response, '/testing/', 302, 200)

    def test_update_view(self):
        response = self.client.get('/test/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        
    def test_update(self):
        response = self.client.post('/test/update/',
                    {
                       'label': 'test2',
                       'user': '1',
                       'display_name': 'test2',
                       'admin_group': '',
                       'url': '',
                     })
        self.assertRedirects(response, '/test2/', 302, 200)
        
    def test_show_view(self):
        response = self.client.get('/test/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('project' in response.context)
        
    def test_delete(self):
        response = self.client.get('/test/delete/')
        self.assertRedirects(response, '/projects/', 302, 200)

    def test_list_repos_view(self):
        response = self.client.get('/projects/test/repos/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('project' in response.context)
        self.assertTrue('repos' in response.context)
        
    def test_create_repo_view(self):
        response = self.client.get('/projects/test/repos/create/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('project' in response.context)
        
    def test_create_repo(self):
        response = self.client.post('/projects/test/repos/create/',
                    {
                        'label': 'test_repo_2',
                        'user': '1',
                        'display_name': 'test repo 2',
                        'path': 'test repo 2',
                        'archs': '1',
                        'project': '1'
                     })
        self.assertRedirects(response, '/test/', 302, 200)
        
    def test_update_repo_view(self):
        response = self.client.get('/projects/test/repos/test_repo/update/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('form' in response.context)
        self.assertTrue('repo' in response.context)
        self.assertTrue('project' in response.context)
        
    def test_update_repo(self):
        response = self.client.post('/projects/test/repos/test_repo/update/',
                    {
                        'label': 'test_repo2',
                        'user': '1',
                        'display_name': 'test repo2',
                        'path': 'test repo2',
                        'archs': '1',
                        'project': '1'
                     })
        self.assertRedirects(response, '/test/', 302, 200)
        
    def test_show_repo_view(self):
        response = self.client.get('/projects/test/repos/test_repo/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('project' in response.context)
        self.assertTrue('repo' in response.context)
        
    def test_delete_repo_view(self):
        response = self.client.get('/projects/test/repos/test_repo/delete/')
        self.assertRedirects(response, '/test/', 302, 200)
