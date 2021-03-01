from main import Song, AudioBook, PodCast


def test_new_song():
    song = Song(song_name='Love Yourself', duration=170).save()
    assert song.song_name == 'Love Yourself'
    assert song.duration == 170


def test_new_audiobook():
    audio = AudioBook(author_name='James Lee',
                      duration=1700,
                      narrator='Keanu Reeves',
                      audiobook_title='The Samaritan',
                      ).save()
    assert audio.author_name == 'James Lee'
    assert audio.duration == 1700
    assert audio.narrator == 'Keanu Reeves'
    assert audio.audiobook_title == 'The Samaritan'


def test_new_podcast():
    podcast = PodCast(host='Peter Crouch',
                      duration=3650,
                      podcast_name='Monday Night Premier League review',
                      ).save()
    assert podcast.podcast_name == 'Monday Night Premier League review'
    assert podcast.host == 'Peter Crouch'
    assert podcast.duration == 3650



