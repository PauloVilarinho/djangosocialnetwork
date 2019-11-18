from django.contrib.auth import get_user_model
from rest_framework import serializers
from socialnetwork.models import *
from .models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email']



class PostSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Post
        fields = ['id','userId', 'title', 'body']

class CommentSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    class Meta:
        model = Comment
        fields = ['id','postId', 'name', 'email', 'body']

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'suite', 'city', 'zipcode']

class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    id = serializers.ReadOnlyField()
    class Meta:
        model = Profile
        fields = ['id','name', 'email','address']

    def create(self, validated_data):
        name = validated_data['name'].split(" ")[0]
        email = validated_data['email']
        password = 'senha'
        new_user = User.objects.create_user(username=name, email=email, password=password)
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        return Profile.objects.create(user=new_user, address=address, **validated_data)

    def update(self,instance,validated_data):
        address_data = validated_data.pop('address')
        address = instance.address
        instance.email = validated_data.get('email', instance.email)
        instance.name = validated_data.get('name', instance.name)
        address.street = address_data.get('street', address.street)
        address.suite = address_data.get('suite', address.suite)
        address.city = address_data.get('city', address.city)
        address.zipcode = address_data.get('zipcode', address.zipcode)
        instance.save()
        address.save()
        return instance

class ProfilePostSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='post-comments-detail'
    )
    id = serializers.ReadOnlyField()
    class Meta:
        model = Profile
        fields = ['id','name', 'email','posts']

class PostCommentSerializer(serializers.ModelSerializer):
    comments = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='comment-detail',
    )
    id = serializers.ReadOnlyField()
    class Meta:
        model = Post
        fields = ['id','userId', 'title', 'body','comments']
