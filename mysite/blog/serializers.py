from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes
from .models import Post, Comment, FavouritePost


class CommentSerializer(serializers.ModelSerializer):
    """Serializer dla komentarzy do postów"""

    class Meta:
        model = Comment
        fields = ['id', 'name', 'email', 'body', 'created', 'active']
        read_only_fields = ['id', 'created', 'active']

    def validate_email(self, value):
        """Walidacja formatu email"""
        if not value:
            raise serializers.ValidationError("Email jest wymagany")
        return value


class PostSerializer(serializers.ModelSerializer):
    """Szczegółowy serializer dla postów z komentarzami"""

    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'body', 'publish',
                 'created', 'updated', 'status', 'comments', 'comments_count']
        read_only_fields = ['id', 'created', 'updated', 'comments']

    @extend_schema_field(OpenApiTypes.INT)
    def get_comments_count(self, obj):
        """Zwraca liczbę aktywnych komentarzy dla postu"""
        return obj.comments.filter(active=True).count()


class PostListSerializer(serializers.ModelSerializer):
    """Uproszczony serializer dla listy postów"""

    author = serializers.StringRelatedField(read_only=True)
    comments_count = serializers.SerializerMethodField()
    excerpt = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'publish',
                 'status', 'comments_count', 'excerpt']

    @extend_schema_field(OpenApiTypes.INT)
    def get_comments_count(self, obj):
        """Zwraca liczbę aktywnych komentarzy dla postu"""
        return obj.comments.filter(active=True).count()

    @extend_schema_field(OpenApiTypes.STR)
    def get_excerpt(self, obj):
        """Zwraca skrócony fragment treści postu (pierwsze 150 znaków)"""
        return obj.body[:150] + '...' if len(obj.body) > 150 else obj.body


class FavouritePostSerializer(serializers.ModelSerializer):
    """Serializer dla ulubionych postów"""

    post = PostListSerializer(read_only=True)

    class Meta:
        model = FavouritePost
        fields = ['user', 'post', 'created']
        read_only_fields = ['created']
