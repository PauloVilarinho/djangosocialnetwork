from rest_framework.views import APIView
from .serializers import *
from .models import *
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

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        profile_post_s = ProfilePostSerializer(profiles, many=True)
        return Response(profile_post_s.data)

class ProfilePostDetailView(APIView):

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request,pk, format=None):
        profile = self.get_object(pk)
        profile_post_s = ProfilePostSerializer(profile)
        return Response(profile_post_s.data)