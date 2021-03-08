import unittest
from main import db, app
import json

audiobook_json = json.dumps({
    'file_type': 'audiobook',
    "author_name": 'John Grisham',
    "narrator": 'Keanu Reeves',
    "audiobook_title": 'The Samaritan',
    "duration": 6509,
})

update_audiobook_json = json.dumps({
    "author_name": 'Sidney Sheldon',
    "narrator": 'Keanu Reeves',
    "audiobook_title": 'The Goosehead',
    "duration": 6509,
})


class BaseCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.get_db()

    def tearDown(self):
        # Delete Database collections after the test is complete
        for collection in self.db.list_collection_names():
            self.db.drop_collection(collection)


class TestAudioBookAPI(BaseCase):

    def test_create_audiobook(self):
        self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        self.assertEqual(201, response.status_code)

    def test_get_audiobook(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        id = response.json['id']
        resp = self.app.get('/api/retrieve/audiobook/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(200, resp.status_code)
        x = resp.get_json()
        self.assertEqual('The Samaritan', x['metadata']['audiobook_title'])
        self.assertEqual('John Grisham', x['metadata']['author_name'])
        self.assertEqual(6509, x['metadata']['duration'])

    def test_update_audiobook(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        id = response.json['id']
        resp = self.app.put('/api/update/audiobook/{}'.format(id), headers={"Content-Type": "application/json"}, data=update_audiobook_json)
        self.assertEqual(200, resp.status_code)
        resp = self.app.get('/api/retrieve/audiobook/{}'.format(id), headers={"Content-Type": "application/json"})
        x = resp.get_json()
        self.assertEqual('The Goosehead', x['metadata']['audiobook_title'])
        self.assertEqual('Sidney Sheldon', x['metadata']['author_name'])
        self.assertEqual(6509, x['metadata']['duration'])

    def test_delete_audiobook(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        id = response.json['id']
        response = self.app.delete('/api/delete/audiobook/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual('Audio deleted successfully', response.json['message'])

    def test_wrong_http_post(self):
        response = self.app.put('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        self.assertEqual(405, response.status_code)

    def test_wrong_http_get(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        id = response.json['id']
        resp = self.app.put('/api/retrieve/audiobook/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(405, resp.status_code)

    def test_wrong_http_put(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        id = response.json['id']
        resp = self.app.get('/api/update/audiobook/{}'.format(id), headers={"Content-Type": "application/json"},
                            data=update_audiobook_json)
        self.assertEqual(405, resp.status_code)

    def test_wrong_http_delete(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=audiobook_json)
        id = response.json['id']
        response = self.app.get('/api/delete/audiobook/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(405, response.status_code)