from rest_framework import serializers
from django.contrib.auth.models import (User)
from core.models import (PostCategory,
                         Post
                         )


class UserPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = (
            'url',
            'name'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    post = UserPostSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'post'
        )


class PostCategorySerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='post-detail'
    )

    class Meta:
        model = PostCategory
        fields = (
            'url',
            'name',
            'pk',
            'post'
        )



class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user')
    post_category = serializers.SlugRelatedField(queryset=PostCategory.objects.all(),
                                                 slug_field='name')

    class Meta:
        model = Post
        fields = (
            'url',
            'post_category',
            'owner',
            'title',
            'content',
            'address',
            'location',
            'createdDate',
            'modifiedDate',
            'image'
        )

