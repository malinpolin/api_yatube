import datetime as dt

from rest_framework import serializers

from posts.models import Post, Group, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    group = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Group.objects.all(),
        required=False
    )
    pub_date = serializers.DateTimeField(
        default=dt.datetime.now,
        read_only=True
    )

    class Meta:
        model = Post
        fields = ('id', 'text', 'author', 'image', 'pub_date', 'group')
        read_only_fields = ('author', 'pub_date')

    def create(self, validated_data):
        return super().create(validated_data)


class GroupSerializer(serializers.ModelSerializer):
    posts = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description', 'posts')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('author', 'created')
