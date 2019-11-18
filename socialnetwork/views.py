from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.request import Request
from .serializers import *
from .models import *
from .permissions import *
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


# Create your views here.

class FileLoad(APIView):

    def post(self, request, format=None):
        posts = request.data['posts']
        comments = request.data['comments']
        profiles = request.data['users']


        for profile in profiles :
            profile_s = ProfileSerializer(data=profile)
            if profile_s.is_valid():
                profile_s.save()

        for post in posts:
            post_s = PostSerializer(data=post)
            if post_s.is_valid():
                post_s.save()

        for comment in comments:
            comment_s = CommentSerializer(data=comment)
            if comment_s.is_valid():
                comment_s.save()

class ProfileView(APIView):

    permission_classes = [IsProfileOrReadOnly]

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        profile_s = ProfileSerializer(profiles, many=True)
        return Response(profile_s.data)

    def post(self, request, format=None):
        profile = request.data
        profile_s = ProfileSerializer(data=profile)
        if profile_s.is_valid():
            profile_s.save()
            return Response(profile_s.data, status=status.HTTP_201_CREATED)
        return Response(profile_s.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetailView(APIView):

    permission_classes = [IsProfileOrReadOnly]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile_s = ProfileSerializer(profile)
        return Response(profile_s.data)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile_s = ProfileSerializer(profile, data=request.data)
        if profile_s.is_valid():
            profile_s.save()
            return Response(profile_s.data)
        return Response(profile_s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile_s = ProfileSerializer(data=request.data)
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_200_OK)


class ProfilePostView(APIView):

    permission_classes = [IsProfileOrReadOnly]

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        serializer_context = {
        'request': request,
        }
        profile_post_s = ProfilePostSerializer(instance= profiles, many=True,context = serializer_context)
        return Response(profile_post_s.data)

class ProfilePostDetailView(APIView):

    permission_classes = [IsProfileOrReadOnly]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        profile = self.get_object(pk)
        serializer_context = {
        'request': request,
        }
        profile_post_s = ProfilePostSerializer(instance= profile,context = serializer_context)
        return Response(profile_post_s.data)


class PostCommentView(APIView):

    permission_classes = [IsProfileOrReadOnly]

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer_context = {
        'request': request,
        }
        post_s = PostCommentSerializer(instance = posts, many=True,context = serializer_context)
        return Response(post_s.data)

    def post(self, request, format=None):
        user_id = request.user.id
        post = request.data
        post['userId'] = user_id
        post_s = PostSerializer(data=post)
        if post_s.is_valid():
            post_s.save()
            return Response(post_s.data, status=status.HTTP_201_CREATED)
        return Response(post_s.errors, status=status.HTTP_400_BAD_REQUEST)

class PostCommentDetailView(APIView):

    permission_classes = [PostIsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        post = self.get_object(pk)
        serializer_context = {
        'request': request,
        }
        post_s = PostCommentSerializer(instance = post,context = serializer_context)
        return Response(post_s.data)

    def put(self, request, pk,format=None):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        post_data = request.data
        post_s = PostSerializer(post, data=post_data)
        if post_s.is_valid():
            post_s.save()
            return Response(post_s.data)
        return Response(post_s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request,pk, format=None):
        post = self.get_object(pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_200_OK)


class CommentView(APIView):

    permission_classes = [CommentIsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        post = self.get_object(pk)
        comment_s = CommentSerializer(post.comments, many=True)
        return Response(comment_s.data)

    def post(self, request,pk, format=None):
        comment = request.data
        comment['postId'] = pk
        comment_s = CommentSerializer(data=comment)
        if comment_s.is_valid():
            comment_s.save()
            return Response(comment_s.data, status=status.HTTP_201_CREATED)
        return Response(comment_s.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):

    permission_classes = [CommentIsOwnerOrReadOnly]

    def get_comment(self, pk):
        try:
            comment =  Comment.objects.get(pk=pk)
            return comment
        except Comment.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        comment = self.get_comment(pk)
        comment_s = CommentSerializer(comment)
        return Response(comment_s.data)

    def put(self, request, pk, format=None):
        comment = self.get_comment(pk)
        self.check_object_permissions(request, comment)
        comment_data = request.data
        comment_s = CommentSerializer(comment, data=comment_data)
        if comment_s.is_valid():
            comment_s.save()
            return Response(comment_s.data)
        return Response(comment_s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment_s = CommentSerializer(data=request.data)
        comment = self.get_comment(pk)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_200_OK)

class ProfileActivityView(APIView):

    permission_classes = [IsProfileOrReadOnly]

    def get(self, request, format=None):
        response = []
        profiles = Profile.objects.all()

        for profile in profiles:
            base = dict()
            base['name'] = profile.name
            base['id'] = profile.id

            count_p = 0
            count_c = 0

            for post in profile.posts.all():
                count_p+=1
                for comment in post.comments.all():
                    count_c+=1

            base['total_posts'] = count_p
            base['total_comments'] = count_c

            response.append(base)

        return Response(response)



class EndpointsView(APIView):

    def get(self,request,format=None):

        data = {

            'profile-list': reverse('profile-list', request=request),
            'profile-post': reverse('profile-post', request=request),
            'post-comments': reverse('post-comments', request=request),
            'profiles-activity': reverse('profiles-activity', request=request),
            'root': reverse('root', request=request),
            'login': reverse('login', request=request),
            'load-files': reverse('load-files', request=request),
        }

        return Response(data, status=status.HTTP_200_OK)


class CustomAuthToken(ObtainAuthToken):

    throttle_scope = 'api-token'
    throttle_classes = [ScopedRateThrottle]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        self.check_throttles(request)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'name': user.username,
            'email': user.email},
            status=status.HTTP_200_OK)
