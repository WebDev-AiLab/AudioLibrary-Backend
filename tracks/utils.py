import json
import os
import io
import re
import urllib

from settings import google_api_key
from tools.shell import run_shell_command
from settings.base import BASE_DIR
from django.core.files import File
from tools.exceptions import WaveformGenerationException
from .models import Artist, Label, Genre, Album, Style
from django.core.files.images import ImageFile
import eyed3
from urllib.request import urlretrieve, urlcleanup
from django.utils.text import slugify
from offers.models import OfferLink
from tools.youtube import get_yt_video_id
from .models import Track
from django.contrib.postgres.search import SearchVector

from django.db.models.functions import Length


def generate_waveform(instance, name):
    if not instance.file:
        return False

    data_directory = os.path.join(BASE_DIR, 'static', 'waveform')
    if not os.path.exists(data_directory):
        os.makedirs(data_directory, exist_ok=True)

    data_path = os.path.join(data_directory, f"{instance.id}.json")

    # now do something
    # todo what about other formats???
    run_shell_command(f"audiowaveform -i {name} --input-format mp3 -o {data_path} --pixels-per-second 6 --bits 8")

    if os.path.exists(data_path):
        instance.waveform = File(open(data_path, 'rb'))
        instance.save()

    else:
        raise WaveformGenerationException('cannot create a waveform file for whatever reason')


def parse_metadata(instance, name):
    if not instance.file:
        return False

    audio = eyed3.load(name)
    # insert all the information
    if not audio.tag:
        print('no tag')
        return

    # title
    instance.title = audio.tag.title
    if not instance.title:
        # replace title with filename if no title
        instance.title = instance.original_file_name

    # also save the original artist
    if audio.tag.artist:
        instance.original_artist = audio.tag.artist

    # i will refactor this code a bit later, for now it doesn't matter
    parsed_artists = _parse_artists(audio.tag, instance.original_artist or instance.original_file_name, instance.title)
    if parsed_artists:
        for artist in parsed_artists:
            instance.artist.add(artist)

    # rating
    rating_regex = r'\(([~^\d!]{1,4})\)'
    rating = re.search(rating_regex, instance.original_file_name)
    if rating and rating[0]:
        instance.rating = re.sub('[\(\)]', '', rating[0])

        # and also replace title and artist, because it can contain this string
        # and use regex, because it can container just fucking everything, there's no system here
        instance.original_artist = re.sub(rating_regex, '', instance.original_artist)
        instance.title = re.sub(rating_regex, '', instance.title)

        # remove ! from rating, because even if it is in the title, it is incorrect
        # again, all this is very weird and just not good, i will redo it normally later, when i finally understand the client's requirements and what the fuck he wants
        # so treat all this code as a temporary solution
        instance.rating = instance.rating.replace('!', '')

    # remixes
    remixes = re.search(r'\([\S\s]+mix\)', instance.original_file_name, re.IGNORECASE)
    if remixes:
        instance.remixes = re.sub('[\(\)]', '', remixes[0])

    # vocal/non-vocal (vocal is by default, so we only search for non-vocal)
    non_vocal = re.search(r'\(non-vocal\)', instance.original_file_name, re.IGNORECASE)
    if non_vocal:
        instance.type = 'Non-Vocal'

    # genre
    genre = _parse_genre(audio.tag, instance.original_file_name)
    if genre:
        instance.genre = genre

    # style
    style = _parse_style(audio.tag, instance.original_file_name, genre)
    if style:
        instance.style = style

    # select default style if style was not set
    if not instance.style:
        instance.style = _select_default_style(genre)

    # album
    if audio.tag.album:
        instance.album = audio.tag.album
    if audio.tag.album_artist:
        instance.album_artist = audio.tag.album_artist

    # create album
    if instance.album:
        obj, created = Album.objects.get_or_create(
            title=audio.tag.album
        )
        if instance.album_artist and not obj.album_artist:
            obj.album_artist = instance.album_artist
        if instance.year and not obj.year:
            obj.year = instance.year

        if instance.artist:
            for artist in instance.artist.all():
                obj.artist.add(artist)

        obj.save()
        # obj, created = Album.objects.get_or_create(
        #     title=audio.tag.album,
        #     original_artist=instance.original_artist
        # )
        # instance.album = obj
        # # and also set artists to this album
        # for artist in instance.artist.all():
        #     obj.artist.add(artist)
        # obj.save()

    # label
    if audio.tag.publisher:
        obj, created = Label.objects.get_or_create(
            name=audio.tag.publisher
        )
        instance.label = obj

    instance.BPM = audio.tag.bpm
    date = audio.tag.getBestDate()
    if date:
        instance.year = date.year
    if instance.year and instance.year >= 2022:
        instance.show_new_releases = True
    instance.duration = audio.info.time_secs
    instance.lyrics = u"".join([i.text for i in audio.tag.lyrics])
    if audio.tag.images and audio.tag.images[0]:
        instance.picture = ImageFile(io.BytesIO(audio.tag.images[0].image_data), name='picture.jpg')

    # instance.artist = audio.tag.artist
    # instance.artist_origin = audio.tag.artist_origin
    # instance.artist_url = audio.tag.artist_url
    # instance.album = audio.tag.album
    # instance.album_artist = audio.tag.album_artist
    # instance.album_type = audio.tag.album_type
    # instance.best_release_date = audio.tag.best_release_date
    # instance.bpm = audio.tag.bpm
    # instance.cd_id = audio.tag.cd_id
    # instance.chapters = audio.tag.chapters
    # instance.clear = audio.tag.clear
    # instance.commercial_url = audio.tag.commercial_url
    # instance.composer = audio.tag.composer
    # instance.copyright = audio.tag.copyright
    # instance.copyright_url = audio.tag.copyright_url
    # instance.disc_num = audio.tag.disc_num
    # instance.internet_radio_url = audio.tag.internet_radio_url
    # instance.lyrics = audio.tag.lyrics
    # instance.non_std_genre = audio.tag.non_std_genre
    # instance.original_artist = audio.tag.original_artist
    # instance.publisher = audio.tag.publisher
    # instance.publisher_url = audio.tag.publisher_url
    # instance.recording_date = audio.tag.recording_date
    # instance.tagging_date = audio.tag.tagging_date

    if Track.objects.filter(original_artist=instance.original_artist, title=instance.title).exists():
        instance.delete()
        return False

    # update slug and save
    instance.set_slug()
    instance.save()
    return True


def _parse_artists(tag, original_file_name, title):
    string = original_file_name

    # upd 03.06.2022
    # before we start, we do something next
    # we also need to search inside the parentheses, because such thing as (Some Artist Extended Remix) also should be processed
    # but ad the same time to avoid problems in title, we don't need to process the rest of the string - only parentheses
    # just append these bad boys to the original string and we're fine
    string_brackets = re.findall(r"\((.*?)\)", title, re.IGNORECASE)
    if string_brackets:
        for string_bracket in string_brackets:
            string += " " + string_bracket

    # todo this code needs optimization if possible
    # think about it
    artists = Artist.objects.all().order_by(Length('name').desc(), 'name')
    artists_valid = []
    for artist in artists:
        result = re.search(r"[\(\s]" + re.escape(artist.name.strip()) + r"[\)\'\s]",
                           string.strip().center(len(string) + 2), re.IGNORECASE)
        if result and result[0]:
            artists_valid.append(artist)
            string = " ".join(string.replace(result[0], ' ').split())
    return artists_valid


def _parse_style(tag, original_file_name, genre):
    if not genre:
        return None

    styles = Style.objects.filter(genre=genre)
    for style in styles:
        regex = r"\(\b" + re.escape(style.name) + r"\b\)"
        result = re.search(regex, original_file_name, re.IGNORECASE)
        if result and result[0]:
            return style


def _parse_genre(tag, original_file_name=None):
    if not tag.genre:
        return None

    genre, created = Genre.objects.get_or_create(
        name=tag.genre.name
    )
    return genre

    # well, we're using treebeard, so using get_or_create is impossible
    # genre = Genre.objects.filter(name__iexact=tag.genre).first()
    # if not genre:
    #     root = Genre.add_root(name=tag.genre)
    #     return Genre.objects.get(pk=root.pk)

    return genre


def process_track(instance):
    # try:
    if instance.file:

        # download the file before doing something
        temp_filename, _ = urlretrieve(instance.file.url)

        if parse_metadata(instance, temp_filename):

            generate_waveform(instance, temp_filename)
            # seems like it is fine?
            instance.celery_upload_status = 3
            # remove temporary files
            # urlcleanup()
            instance.save()
    else:
        raise WaveformGenerationException(f"No track file for {instance.id}")

    # except:
    #     instance.celery_upload_status = 2


def _select_default_style(genre):
    return Style.objects.filter(genre=genre, is_default=True).first()


def parse_links(instance):
    # step 1: find all the links from string
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', instance.text)

    # step 2: check the source
    if urls:
        for url in urls:
            title = ''
            source = None
            # 1. check if YouTube
            youtube_id = get_yt_video_id(url)
            if youtube_id:
                title = fetch_title_youtube(youtube_id)
                source = 'youtube'

            # 3. finally save
            OfferLink.objects.create(
                offer=instance,
                link=url,
                title=title,
                source=source
            )


def fetch_title_youtube(video_id):
    params = {'id': video_id, 'key': google_api_key,
              'fields': 'items(id,snippet(channelId,title,categoryId),statistics)',
              'part': 'snippet,statistics'}

    url = 'https://www.googleapis.com/youtube/v3/videos'

    query_string = urllib.parse.urlencode(params)
    url = url + "?" + query_string

    with urllib.request.urlopen(url) as response:
        response_text = response.read()
        data = json.loads(response_text.decode())
        return data['items'][0]['snippet']['title']


def create_search_vectors(track):
    # temporary
    title_search_vector = SearchVector('title')
    original_artist_search_vector = SearchVector('original_artist')

    if title_search_vector != track.title_search_vector or original_artist_search_vector != track.original_artist_search_vector:
        track.title_search_vector = title_search_vector
        track.original_artist_search_vector = original_artist_search_vector
        return track.save()
