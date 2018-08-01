from core.models import (PostCategory,
                         Post)
from core.serializers import (UserSerializer,
                              PostCategorySerializer,
                              PostSerializer)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.parsers import (MultiPartParser,
                                    FormParser)
from django.contrib.auth.models import User
from rest_framework import permissions
from core.permissions import IsOwnerOrReadOnly
import geocoder
# Create your views here.


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-detail'


class PostCategoryList(generics.ListCreateAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
    name = 'postcategory-list'


class PostCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
    name = 'postcategory-detail'


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-list'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        address = serializer.initial_data['address']
        g = geocoder.google(address)
        lat = g.latlng[0]
        lng = g.latlng[1]
        point = 'POINT('+str(lat)+' ' + str(lng)+')'
        serializer.save(location=point, owner=self.request.user, image=self.request.data.get('image'))


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-detail'
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class APIRoot(generics.GenericAPIView):
    name = 'api'

    def get(self, request, *args, **kwargs):
        return Response({
            # 'user': reverse(UserList.name, request=request),
            'post-category': reverse(PostCategoryList.name, request=request),
            'post': reverse(PostList.name, request=request)
        })