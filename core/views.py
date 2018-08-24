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

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
# Create your views here.

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    name = 'user-list'
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]


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
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        address = serializer.initial_data['address']
        try:
            g = geocoder.google(address)
            lat = g.latlng[0]
            lng = g.latlng[1]
            point = 'POINT('+str(lat)+' ' + str(lng)+')'
        except:
            point = 'POINT(' + str(10.7770983) + ' ' + str(106.693229) + ')'
        serializer.save(location=point, image=self.request.data.get('image'))
        # serializer.save(location=point, owner=self.request.user, image=self.request.data.get('image'))


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    name = 'post-detail'
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)


class APIRoot(generics.GenericAPIView):
    name = 'api'

    def get(self, request, *args, **kwargs):
        return Response({
            'user': reverse(UserList.name, request=request),
            'post-category': reverse(PostCategoryList.name, request=request),
            'post': reverse(PostList.name, request=request)
        })