"""
$ coverage run manage.py test mirrorlist
$ coverage report --include=./apps/mirrorlist/views.py
Name                    Stmts   Miss  Cover
-------------------------------------------
apps/mirrorlist/views      57     31    46%

"""

from django.test import TestCase

class MirrorListViewsTestCases(TestCase):
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
                        'label': 'test',
                        'user': '1',
                        'display_name': 'test',
                        'path': 'test',
                        'archs': '1',
                        'project': '1'
                     })
    
    def test_mirror_list_404(self):
        response = self.client.get('/mirrorlist/')
        self.assertEqual(response.status_code, 404)

    def test_mirror_list(self):
        response = self.client.get('/mirrorlist/?repo=test&arch=i386')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('resources' in response.context)
        self.assertTrue('location' in response.context)