from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
import datetime

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'your_database',
    'host': 'localhost',
    'port': 27017,
}
db = MongoEngine()
db.init_app(app)


class Song(db.Document):
    song_name = db.StringField(max_length=100, required=True)
    duration = db.IntField(required=True)
    uploaded_time = db.DateTimeField(required=True, default=datetime.datetime.utcnow())


class AudioBook(db.Document):
    audiobook_title = db.StringField(required=True, max_length=100)
    author_name = db.StringField(required=True, max_length=100)
    narrator = db.StringField(required=True, max_length=100)
    duration = db.IntField(required=True)
    uploaded_time = db.DateTimeField(required=True, default=datetime.datetime.utcnow())


class PodCast(db.Document):
    podcast_name = db.StringField(required=True)
    duration = db.IntField(required=True)
    uploaded_time = db.DateTimeField(required=True, default=datetime.datetime.utcnow())
    host = db.StringField(required=True)
    participants = db.ListField(db.StringField())


@app.route('/api/create', methods=['POST', ])
def create_audio():
    body = request.get_json()
    file = body['file_type']
    if file == 'song' and 'song_name' in body and 'duration' in body:  # use file = file.lower() instead
        song = Song(song_name=body['song_name'], duration=body['duration']).save()
        data = {
            "id": str(song.id),
            "message": 'Song Successfully created'
        }
        return jsonify(data), 201
    if file == 'audiobook' and 'author_name' in body and 'duration' in body and 'audiobook_title' in body and \
            'duration' in body and 'narrator' in body:
        audio = AudioBook(author_name=body['author_name'],
                          duration=body['duration'],
                          narrator=body['narrator'],
                          audiobook_title=body['audiobook_title'],).save()
        data = {
            "id": str(audio.id),
            "message": 'Audiobook Successfully created'
        }
        return jsonify(data), 201
    if file == 'podcast' and 'podcast_name' in body and 'duration' in body and 'host' in body:
        podcast = PodCast(host=body['host'],
                          duration=body['duration'],
                          podcast_name=body['podcast_name']).save()
        data = {
            "id": str(podcast.id),
            "message": 'Podcast Successfully created'
        }
        return jsonify(data), 201
    data = {
        "message": 'Check Parameters'
    }
    return jsonify(data)


@app.route('/api/retrieve/<string:file>/<string:id>', methods=['GET', ])
def get_audio(file, id):
    file = file.lower()
    if file == 'song':
        try:
            song = Song.objects.get(id=id)
            data = {
                "message": 'Song Retrieved successfully',
                'file_type': file,
                'metadata': {
                    "song_name": song.song_name,
                    "duration": song.duration,
                    "uploaded_time": song.uploaded_time
                }
            }
            return jsonify(data), 200
        except Song.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404

    if file == 'audiobook':
        try:
            audio = AudioBook.objects.get(id=id)
            data = {
                "message": 'Audio Retrieved successfully',
                'file_type': file,
                'metadata': {
                    "author_name": audio.author_name,
                    "narrator": audio.narrator,
                    "audiobook_title": audio.audiobook_title,
                    "duration": audio.duration,
                    "uploaded_time": audio.uploaded_time,
                }
            }
            return jsonify(data), 200
        except PodCast.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404
    if file == 'podcast':
        try:
            podcast = PodCast.objects.get(id=id)
            data = {
                "message": 'Podcast Retrieved successfully',
                'file_type': file,
                'metadata': {
                    "host": podcast.host,
                    "podcast_name": podcast.podcast_name,
                    "duration": podcast.duration,
                    "uploaded_time": podcast.uploaded_time,
                    "participants": podcast.participants
                }
            }
            return jsonify(data)
        except PodCast.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404
    return {'message': 'Invalid Parameter'}


@app.route('/api/update/<string:file>/<string:id>', methods=['PUT', ])
def update_audio(file, id):
    file = file.lower()
    body = request.get_json()
    if file == 'song':
        try:
            song = Song.objects.get(id=id)
            song.update(**body)
            data = {
                "message": 'Song Retrieved successfully',
                'file_type': file,
                'metadata': {
                    "song_name": song.song_name,
                    "duration": song.duration,
                    "uploaded_time": song.uploaded_time
                }
            }
            return jsonify(data), 200
        except Song.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404

    if file == 'audiobook':
        try:
            audio = AudioBook.objects.get(id=id)
            audio.update(**body)
            data = {
                "message": 'Song Retrieved successfully',
                'file_type': file,
                'metadata': {
                    "author_name": audio.author_name,
                    "narrator": audio.narrator,
                    "audiobook_title": audio.audiobook_title,
                    "duration": audio.duration,
                    "uploaded_time": audio.uploaded_time,
                }
            }
            return jsonify(data), 200
        except AudioBook.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404
    if file == 'podcast':
        try:
            podcast = PodCast.objects.get(id=id)
            podcast.update(**body)
            data = {
                "message": 'Podcast Retrieved successfully',
                'file_type': file,
                'metadata': {
                    "host": podcast.host,
                    "podcast_name": podcast.podcast_name,
                    "duration": podcast.duration,
                    "uploaded_time": podcast.uploaded_time,
                    "participants": podcast.participants
                }
            }
            return jsonify(data), 200
        except PodCast.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404
    return {'message': 'Invalid Parameter'}


@app.route('/api/delete/<string:file>/<string:id>', methods=['DELETE', ])
def delete_audio(file, id):
    file = file.lower()
    if file == 'song':
        try:
            song = Song.objects.get(id=id)
            song.delete()
            data = {
                "message": 'Song deleted successfully',
                'file_type': file,
                'metadata': {
                    "song_name": song.song_name,
                }
            }
            return jsonify(data)
        except Song.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404

    if file == 'audiobook':
        try:
            audio = AudioBook.objects.get(id=id)
            audio.delete()
            data = {
                "message": 'Audio deleted successfully',
                'file_type': file,
                'metadata': {
                    "audiobook_title": audio.audiobook_title
                }
            }
            return jsonify(data)
        except PodCast.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404
    if file == 'podcast':
        try:
            podcast = PodCast.objects.get(id=id)
            podcast.delete()
            data = {
                "message": 'Podcast deleted successfully',
                'file_type': file,
                'metadata': {
                    "podcast_name": podcast.podcast_name,
                }
            }
            return jsonify(data)
        except PodCast.DoesNotExist:
            data = {
                'message': 'Not Found'
            }
            return jsonify(data), 404
    return {'message': 'Invalid Parameter'}


if __name__ == "__main__":
    app.run(port=5000, debug=True)