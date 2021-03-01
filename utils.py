import datetime
import json


song_json = {
    'file_type': 'song',
    'song_name': 'Love yourself',
    'duration': 190,

}


update_song_json = {
    'file_type': 'song',
    'song_name': 'Me and You',
    'duration': 197,
    'uploaded_time': datetime.datetime.utcnow()

}


audiobook_json = {
        'file_type': 'audiobook',
        "author_name": 'John Grisham',
        "narrator": 'Keanu Reeves',
        "audiobook_title": 'The Samaritan',
        "duration": 6509,
}


update_audiobook_json = {
        'file_type': 'audiobook',
        "author_name": 'Sidney Sheldon',
        "narrator": 'Keanu Reeves',
        "audiobook_title": 'The Goosehead',
        "duration": 6509,
        "uploaded_time": datetime.datetime.utcnow()
}


podcast_json = {
        'file_type': 'podcast',
        "host": 'Peter Crouch',
        "podcast_name": 'Monday Night Premier League review',
        "duration": 3660,
}


update_podcast_json = {
        'file_type': 'podcast',
        "host": 'Pete Crouch',
        "podcast_name": 'Daily Night Premier League review',
        "duration": 3500,
        "uploaded_time": datetime.datetime.utcnow()
}