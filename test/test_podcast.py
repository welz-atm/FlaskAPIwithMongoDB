import unittest
from main import db, app
import json

podcast_json = json.dumps({
        'file_type': 'podcast',
        "host": 'Peter Crouch',
        "podcast_name": 'Monday Night Premier League review',
        "duration": 3660,
})

update_podcast_json = json.dumps({
        "host": 'Peter Crouch',
        "podcast_name": 'Monday Night Football League review',
        "duration": 3660,
})


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)


class TestPodcastAPI(BaseCase):

    def test_create_podcast(self):
        self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        self.assertEqual(201, response.status_code)

    def test_get_podcast(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        id = response.json['id']
        resp = self.app.get('/api/retrieve/podcast/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(200, resp.status_code)
        x = resp.get_json()
        self.assertEqual('Peter Crouch', x['metadata']['host'])
        self.assertEqual('Monday Night Premier League review', x['metadata']['podcast_name'])
        self.assertEqual(3660, x['metadata']['duration'])

    def test_update_podcast(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        id = response.json['id']
        resp = self.app.put('/api/update/podcast/{}'.format(id), headers={"Content-Type": "application/json"}, data=update_podcast_json)
        self.assertEqual(200, resp.status_code)
        resp = self.app.get('/api/retrieve/podcast/{}'.format(id), headers={"Content-Type": "application/json"})
        x = resp.get_json()
        self.assertEqual('Peter Crouch', x['metadata']['host'])
        self.assertEqual('Monday Night Football League review', x['metadata']['podcast_name'])
        self.assertEqual(3660, x['metadata']['duration'])

    def test_delete_podcast(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        id = response.json['id']
        response = self.app.delete('/api/delete/podcast/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual('Podcast deleted successfully', response.json['message'])

    def test_wrong_http_post(self):
        response = self.app.put('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        self.assertEqual(405, response.status_code)

    def test_wrong_http_get(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        id = response.json['id']
        resp = self.app.put('/api/retrieve/podcast/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(405, resp.status_code)

    def test_wrong_http_put(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        id = response.json['id']
        resp = self.app.get('/api/update/podcast/{}'.format(id), headers={"Content-Type": "application/json"},
                            data=update_podcast_json)
        self.assertEqual(405, resp.status_code)

    def test_wrong_http_delete(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=podcast_json)
        id = response.json['id']
        response = self.app.get('/api/delete/podcast/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(405, response.status_code)