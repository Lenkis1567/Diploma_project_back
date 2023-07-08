from django.forms import fields
from django.http import JsonResponse, response
from django.urls import reverse_lazy
from django.views import generic
from .models import Age_range, Books, Library, UserProfile, Message, RentsBook
from django.shortcuts import render
from django.views.generic import CreateView, ListView
from rest_framework import generics, viewsets, permissions
from .serializers import BooksSerializer, Age_rangeSerializer, RentsAddSerializer, BoobByGglIdSerializer, RentsBookSerializer, LibraryListSerializer, LibraryAddSerializer, LibrarySeachBookSerializer, MessageListSerializer, MessageAddSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.exceptions import NotFound
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.db.models import Q
import json
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import timezone
from django.http import Http404
from rest_framework import status

# Create your views here.


def homepage(request):
    return render(request, 'main/homepage.html')

class BooksList(ListView):
    model = Books
    fields = '__all__'
    template_name = 'main/books_list.html'
    

class Book_Add(CreateView):
    model = Books
    fields = '__all__'
    template_name = 'main/book_add.html'
    success_url = reverse_lazy ('booklist_path')

class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        try:
            profile = UserProfile.objects.get(user=token.user_id)
            profile_pk = profile.pk
        except:
            profile_pk = 0
        return Response({'token': token.key, 'id': token.user_id, 'profile_id':profile_pk})

class BooksApi(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class Age_rangeApi(generics.ListAPIView):
    queryset = Age_range.objects.all()
    serializer_class = Age_rangeSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BookByGglId(generics.RetrieveAPIView):
    queryset = Books.objects.all()
    serializer_class = BoobByGglIdSerializer
    lookup_field = 'googl_id'
    lookup_url_kwarg = 'id'
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class LibraryListAPI(generics.ListAPIView):
    queryset = Library.objects.all()
    serializer_class = LibraryListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class LibraryCreateAPI(generics.CreateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibraryAddSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
            user_id = request.query_params.get('user_id', '')
            print("Мы ищем пользователя с id", user_id)
            try:
                # user_id=request.GET.get('user_id', '')
                user = User.objects.get(id=user_id)
                print("Мы ищем пользователя с previose id ", user)
                user_profile = UserProfile.objects.get(user=user)
            except (User.DoesNotExist, UserProfile.DoesNotExist):
                raise NotFound("No such user or user profile found")
            print("user_id")
        
            profile_data = {
                'first_name': user_profile.first_name,
                'last_name': user_profile.last_name,
                'Email': user_profile.email,
                'phone': user_profile.phone,
                'city': user_profile.city,
                'address': user_profile.address,
                'geo_latitudes': user_profile.geo_latitudes,
                'geo_longitude': user_profile.geo_longitude,
            }
        
            return Response(profile_data)

    
    def post (self, request):
        print("Мы в профиле пользователя",request.data)
        try:
            profile_info = request.data
            user = request.user
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.first_name    = profile_info['first_name']
            user_profile.last_name     = profile_info['last_name']
            user_profile.email         = profile_info['Email']
            user_profile.phone         = profile_info['phone']
            user_profile.city          = profile_info['city']
            user_profile.address       = profile_info['address']
            user_profile.geo_latitudes = profile_info['geo_latitudes']
            user_profile.geo_longitude = profile_info['geo_longitude']
            user_profile.save()
            return Response ({'ok':True, 'user_profile_id':user_profile.id, 'message':'User profile created successfully'})
        except:
            return Response ({'ok':False, 'message':'Error creating user profile'})
        

class LibrarySeachBook (APIView):
    def get(self, request):
        title = request.GET.get('title', '')
        author = request.GET.get('author', '')
        age_range = request.GET.get('age_range', '')
        print (title, author, age_range)

        book_list = Library.objects.all()
        if title != ' ':
            print ('Ищем по заголовку', title)
            book_list = book_list.filter(book__title__icontains=title)
        if author != ' ':
            print ('Ищем по заголовку', title)
            book_list = book_list.filter(book__author__icontains=author)
        search_data = []
        for book in book_list:
            search_data.append({
                'id': book.pk,
                'titel': book.book.title,
                'author' : book.book.author,
                'img' : book.book.img,
                'name' : ' ' if book.user.first_name is None else book.user.first_name + \
                        ' ' + ' ' if  book.user.last_name is None else book.user.last_name,
                'addres' : ' ' if book.user.city is None else book.user.city + \
                        ' ' + ' ' if  book.user.address is None else book.user.address,
                'phone' : book.user.phone,
                'email' : book.user.email,

            })
        print (search_data)
        json_data = json.dumps(search_data)
        return HttpResponse(json_data, content_type='application/json')
    
        # return JsonResponse(search_data)
        # ser_data = LibrarySeachBookSerializer(search_data, many=True)
        # print(ser_data.data)
        # return (response(ser_data.validated_data))



class MessagesListAPI(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class MessagesCreateAPI(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageAddSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RentsListAPI(generics.ListAPIView):
    queryset = RentsBook.objects.all()
    serializer_class = RentsBookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RentsCreateAPI(generics.CreateAPIView):
    queryset = RentsBook.objects.all()
    serializer_class = RentsAddSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class RentsChangeAPI(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def put(self, request, id):
        print('PUT REQUEST FOR RENT', request)
        rent_id = request.data.get('id')
        try:
            rent = RentsBook.objects.get(pk=id)
            print('rent: ', rent)
            rent.end_date = timezone.now()
            rent.save()
            print(rent)
            return Response({'ok': True}, status=status.HTTP_200_OK)
        except RentsBook.DoesNotExist:
            raise Http404("Rent not found")
        





class MessagesSearch(APIView):
    def get(self, request):
        owner = request.GET.get('owner', '')
        rent_user = request.GET.get('rent_user', '')
        book = request.GET.get('book', '')
        print(owner, rent_user)

        message_list = Message.objects.all()
        # print("messages---------------------", message_list)
        if owner != '':
            print('searching by the owner', owner)
            message_list = message_list.filter(owner__user__username__icontains=owner)
        elif rent_user != '':
            print('searching by the rent_user', rent_user)
            message_list = message_list.filter(rent_user__user__username__icontains=rent_user)
        elif book != '':
            message_list = message_list.filter(book__id=book)

            
        search_data = []
        for message in message_list:
            search_data.append({
                'id': message.pk,
                'owner': message.owner.user.username,
                'owner_id': message.owner.id,
                'rent_user': message.rent_user.user.username,
                'rent_user_id': message.rent_user.id,
                'text': message.text,
                'date_sent': message.date_sent,
                'date_read': message.date_read,
                'read': message.read,
                'book': message.book.book.title,
                'book_id':message.book.id,
                'sender':message.sender.id
            })

        print("Search data", search_data)
        json_data = json.dumps(search_data, cls=DjangoJSONEncoder)
        return HttpResponse(json_data, content_type='application/json')
    
class MessagesChange(APIView):
    def put(self, request):
        print('PUT REQUEST', request)
        message_id = request.data.get('id')
        try:
            message = Message.objects.get(pk=message_id)
            message.date_read = timezone.now()
            message.read = True
            message.save()
            print(message)
            return HttpResponse(status=200)
        except Message.DoesNotExist:
            return HttpResponse(status=404)
        

