from django.shortcuts import get_object_or_404
from mutagen.easyid3 import EasyID3
from rest_framework import serializers
from tinytag import TinyTag

from .models import Track, Artist, Style, Label, ArtistImage, Submission, Rating
from .validators import validate_track_upload
# from tools.mixins import PictureThumbnailSerializer
from interactions.models import Play, Vote, Comment
from accounts.models import User
from tools.baseserializers import S3ImageModelSerializer
from tools.validators import grecaptcha_validator
from accounts.serializers import UserPublicLightSerializer
import mutagen

class CreateTrackSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True, validators=(validate_track_upload,))

    def _save_meta(self, obj, audio):
        obj.title = audio.title
        obj.album = audio.album
        obj.year = audio.year
        try:
            artist = get_object_or_404(Artist, name=audio.artist)
            obj.artist.add(artist)
            obj.save()
            return obj
        except:
            Artist.objects.create(name=audio.artist)
            artist = get_object_or_404(Artist, name=audio.artist)
            print(obj, obj.artist)
            obj.artist.add(artist)
            obj.save()
            return obj




    def create(self, validated_data):
        track = Track.objects.create(
            file=validated_data['file'],
        )
        audio = TinyTag.get(f'media/{track.file}')
        print(audio)
        return self._save_meta(track, audio)


    class Meta:
        model = Track
        fields = ['id', 'file']


class ArtistImageSerializer(S3ImageModelSerializer):
    class Meta:
        model = ArtistImage
        fields = '__all__'


class ArtistListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'name', 'slug', 'picture', 'picture_thumbnail', 'visible']


class ArtistSerializer(serializers.ModelSerializer):
    artist_images = ArtistImageSerializer(many=True, read_only=True)

    class Meta:
        model = Artist
        fields = '__all__'


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = '__all__'


class TrackListingSerializer(serializers.ModelSerializer):
    artist = ArtistListingSerializer(many=True, read_only=True)
    label = LabelSerializer(read_only=True)
    # album = serializers.SerializerMethodField()
    genre = serializers.SerializerMethodField()
    style = serializers.SerializerMethodField()

    # extra
    plays_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    # personal
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Track
        exclude = []

    def get_comments_count(self, obj):
        return obj.comments_count

    def get_plays_count(self, obj):
        return obj.plays_count

    # def get_album(self, obj):
    #     return obj.album.title if obj.album else ""

    def get_genre(self, obj):
        # return obj.genre.name if obj.genre else ""
        return None

    def get_style(self, obj):
        return obj.style.name if obj.style else ""

    def get_is_liked(self, obj):
        return False
        # user = self.context['request'].user
        # if not user.is_anonymous:
        #     res = Vote.objects.filter(user=user, track=obj).first()
        #     if res:
        #         return True
        # return False

    # def get_genre(self, obj):
    #
    #     # slow and not good, will improve this later
    #
    #     if not obj.genre:
    #         return ""
    #
    #     root = obj.genre.get_ancestors().first()
    #     if not root:
    #         return obj.genre.name
    #
    #     return f"{root.name}/{obj.genre.name}"


class CreatePlaySerializer(serializers.ModelSerializer):
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all())
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True)
    ip = serializers.CharField(max_length=46)

    class Meta:
        model = Play
        fields = ['track', 'ip', 'user']


class CreateCommentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all())
    token = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])
    text = serializers.CharField(write_only=True, required=True, max_length=2048)
    type = serializers.CharField(write_only=True, required=True, max_length=2048)

    class Meta:
        model = Comment
        fields = ['user', 'track', 'token', 'text', 'type']

    def create(self, validated_data):
        return Comment.objects.create(
            type=validated_data['type'],
            user=validated_data['user'],
            track=validated_data['track'],
            text=validated_data['text']
        )


class CreateCommentArtistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    artist = serializers.PrimaryKeyRelatedField(queryset=Artist.objects.all())
    token = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])
    text = serializers.CharField(write_only=True, required=True, max_length=2048)
    type = serializers.CharField(write_only=True, required=True, max_length=2048)

    class Meta:
        model = Comment
        fields = ['user', 'artist', 'token', 'text', 'type']

    def create(self, validated_data):
        return Comment.objects.create(
            type=validated_data['type'],
            user=validated_data['user'],
            artist=validated_data['artist'],
            text=validated_data['text']
        )


class CreateLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    track = serializers.PrimaryKeyRelatedField(queryset=Track.objects.all())
    token = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])

    class Meta:
        model = Vote
        fields = ['user', 'track', 'token']

    def create(self, validated_data):
        return Vote.objects.create(
            user=validated_data['user'],
            track=validated_data['track']
        )


class StyleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Style
        fields = ['id', 'name', 'picture', 'picture_thumbnail', 'description']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


# class ArtistSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Artist
#         fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = UserPublicLightSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'created', 'track', 'artist', 'user', 'text', 'at']


class SubmissionSerializer(serializers.ModelSerializer):
    text = serializers.CharField(max_length=4096, required=True)
    # file = serializers.FileField(write_only=True, required=True, validators=(validate_track_upload,))
    # title = serializers.CharField(max_length=1024, required=True)
    # name = serializers.CharField(max_length=1024, required=True)
    # email = serializers.CharField(max_length=1024, required=True)
    token = serializers.CharField(write_only=True, required=True, validators=[grecaptcha_validator()])
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Submission
        fields = ['text', 'token', 'user']

    def create(self, validated_data):
        return Submission.objects.create(
            # title=validated_data['title'],
            # name=validated_data['name'],
            text=validated_data['text'],
            user=validated_data['user'],
            # email=validated_data['email'],
            # file=validated_data['file']
        )
