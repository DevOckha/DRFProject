from captcha.models import CaptchaStore
from django.contrib.auth.hashers import make_password
from .models import User, Article, Comment
from .permissions import UserPermission, IsAuthorOrReadOnly
from .serializers import UserSerializer, ArticleSerializer, CommentSerializer
from rest_framework import parsers, permissions, renderers, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView


@api_view(['GET'])
@permission_classes((AllowAny,))
def api_root(request, format=None):
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'articles': reverse('article-list', request=request, format=format),
        'comments': reverse('comment-list', request=request, format=format)
    })


class UserViewSet(viewsets.ModelViewSet):
    
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (UserPermission, )


    def create(self, request, *args, **kwargs):
        if 'captcha-value' not in self.request.data or 'captcha-key' not in self.request.data:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        captcha_key = self.request.data['captcha-key']
        captcha_value = self.request.data['captcha-value']

        try:
            captcha = CaptchaStore.objects.get(challenge=captcha_value, hash_key=captcha_key)
            captcha.delete()
        except:
            return Response({'state':False, 'code':1, 'message':'Captcha input is not correct'})
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        serializer.save(password, is_active=True)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        if 'email' in self.request.data or 'password' in self.request.data or 'is_active' in self.request.data:
            if 'original-password' not in self.request.data:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if instance.check_password(self.request.data['original-password']) == False:
                return Response({'state':False, 'code':1, 'message':'Password is not correct'}, status=status.HTTP_200_OK)
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer=serializer)

        return Response(serializer.data)
    
    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(self.request.data['password'])
            serializer.save(password)
        else:
            serializer.save()


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        
        serializer.save(author=self.request.user, article_id = int(self.request.data['article_id']))