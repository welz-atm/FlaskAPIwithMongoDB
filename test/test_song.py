import unittest
from main import db, app
import json

song_json = json.dumps({
    'file_type': 'song',
    'song_name': 'Love yourself',
    'duration': 190,
})

update_song_json = json.dumps({
    'song_name': 'Love yourselves',
    'duration': 190,
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

    def test_create_song(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=song_json)
        self.assertEqual(201, response.status_code)

    def test_get_song(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=song_json)
        id = response.json['id']
        resp = self.app.get('/api/retrieve/song/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(200, resp.status_code)
        x = resp.get_json()
        self.assertEqual('Love yourself', x['metadata']['song_name'])
        self.assertEqual(190, x['metadata']['duration'])

    def test_update_song(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=song_json)
        id = response.json['id']
        resp = self.app.put('/api/update/song/{}'.format(id), headers={"Content-Type": "application/json"}, data=update_song_json)
        self.assertEqual(200, resp.status_code)
        resp = self.app.get('/api/retrieve/song/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(200, resp.status_code)
        x = resp.get_json()
        self.assertEqual('Love yourselves', x['metadata']['song_name'])
        self.assertEqual(190, x['metadata']['duration'])

    def test_delete_song(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=song_json)
        id = response.json['id']
        response = self.app.delete('/api/delete/song/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(200, response.status_code)
        self.assertEqual('Song deleted successfully', response.json['message'])

    def test_wrong_http_post(self):
        response = self.app.put('/api/create', headers={"Content-Type": "application/json"}, data=song_json)
        self.assertEqual(405, response.status_code)

    def test_wrong_http_get(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=song_json)
        id = response.json['id']
        resp = self.app.put('/api/retrieve/song/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(405, resp.status_code)

    def test_wrong_http_put(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=song_json)
        id = response.json['id']
        resp = self.app.get('/api/update/song/{}'.format(id), headers={"Content-Type": "application/json"},
                            data=update_song_json)
        self.assertEqual(405, resp.status_code)

    def test_wrong_http_delete(self):
        response = self.app.post('/api/create', headers={"Content-Type": "application/json"}, data=song_json)
        id = response.json['id']
        response = self.app.get('/api/delete/song/{}'.format(id), headers={"Content-Type": "application/json"})
        self.assertEqual(405, response.status_code)