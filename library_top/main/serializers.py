from django.forms import fields
from .models import Books, Age_range, Library, UserProfile, Message, RentsBook
from rest_framework import serializers
from django.contrib.auth.models import User


class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class Age_rangeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Age_range
        fields = '__all__'

class BoobByGglIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model=UserProfile
        fields = '__all__'

class LibraryListSerializer(serializers.ModelSerializer):
    book = BooksSerializer ()
    user = UserProfileSerializer ()
    class Meta:
        model = Library
        fields = '__all__'


class LibraryAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = '__all__'



class LibrarySeachBookSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    titel = serializers.CharField()
    author = serializers.CharField()
    img = serializers.CharField()
    name = serializers.CharField()
    addres = serializers.CharField()
    phone = serializers.CharField()
    email = serializers.CharField()




class RentsBookSerializer(serializers.ModelSerializer):
    rent_user = UserProfileSerializer()
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    book = LibraryListSerializer()

    class Meta:
        model = RentsBook
        fields = '__all__'

class RentsAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentsBook
        fields = '__all__'


class MessageListSerializer(serializers.ModelSerializer):
    book = LibraryListSerializer()
    owner = UserProfileSerializer ()
    rent_user = UserProfileSerializer ()
    class Meta:
        model = Message
        fields = '__all__'

class MessageAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class MessageSeachSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    book = LibraryListSerializer()
    rent_user = UserProfileSerializer ()
    owner = UserProfileSerializer ()
    text = serializers.CharField()
    date_sent = serializers.DateTimeField()
    date_read = serializers.DateTimeField()
    read = serializers.BooleanField()
  
