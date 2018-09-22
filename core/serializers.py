from rest_framework import serializers
from django.contrib.auth.models import (User)
from core.models import (PostCategory, Post, Images)

class UserPostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = (
            'url',
            'name'
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    post = UserPostSerializer(many=True, read_only=True)
    # post = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='post-detail')
    # password = serializers.CharField(write_only=True)
    #
    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data['username']
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

    class Meta:
        model = User
        fields = (
            'url',
            'pk',
            'username',
            'post',
            # 'password'
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

class ImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Images
        fields = (
            'image',
            'uploaded',
            'posts'
        )

class PostSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.user')
    post_category = serializers.SlugRelatedField(queryset=PostCategory.objects.all(),
                                                 slug_field='name')
    images = ImagesSerializer(
        many=True,
    )

    class Meta:
        model = Post
        fields = (
            'url',
            'id',
            'post_category',
            'owner',
            'title',
            'content',
            'address',
            'location',
            'createdDate',
            'modifiedDate',
            'images'
        )

    def create(self, validated_data):
        images_data = validated_data.pop('images')
        post = Post.objects.create(**validated_data)
        for image_data in images_data:
            Images.objects.create(posts=post, **image_data)
        return post