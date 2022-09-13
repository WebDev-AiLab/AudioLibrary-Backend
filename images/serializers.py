from rest_framework import serializers
from .models import S3Image


class S3ImageModelSerializer(serializers.ModelSerializer):
    # todo remove fucking indian code!

    s3_source = serializers.SerializerMethodField()
    s3_image_1920 = serializers.SerializerMethodField()
    s3_image_1280 = serializers.SerializerMethodField()
    s3_image_960 = serializers.SerializerMethodField()
    s3_image_720 = serializers.SerializerMethodField()
    s3_image_480 = serializers.SerializerMethodField()
    s3_image_320 = serializers.SerializerMethodField()

    def get_s3_source(self, instance):
        return instance.s3_source.url

    def get_s3_image_1920(self, instance):
        return instance.s3_image_1920.url

    def get_s3_image_1280(self, instance):
        return instance.s3_image_1280.url

    def get_s3_image_960(self, instance):
        return instance.s3_image_960.url

    def get_s3_image_720(self, instance):
        return instance.s3_image_720.url

    def get_s3_image_480(self, instance):
        return instance.s3_image_480.url

    def get_s3_image_320(self, instance):
        return instance.s3_image_320.url

    class Meta:
        model = S3Image
        fields = ['id', 's3_source', 's3_source_width', 's3_source_height', 's3_image_1920', 's3_image_1280',
                  's3_image_960',
                  's3_image_720', 's3_image_480',
                  's3_image_320']
