
from django.contrib import admin
from django.urls import path, include, re_path
from .views import Book_Add, BooksList, homepage, BooksApi, Age_rangeApi, BookByGglId 
from .views import CustomObtainAuthToken, LibraryListAPI, MessagesChange, RentsCreateAPI, RentsListAPI, RentsChangeAPI, UserProfileView, LibraryCreateAPI, LibrarySeachBook, MessagesListAPI, MessagesCreateAPI, MessagesSearch
from rest_framework import routers
# from django.conf.urls import url


router = routers.SimpleRouter()
router.register(r'book', BooksApi)
# routerLbr = routers.SimpleRouter()
# routerLbr.register(r'library', LibraryAPI)


urlpatterns = [
    path('', homepage, name='homepage_path'),
      
    path('bookslist/',     BooksList.as_view(), name='booklist_path'),
    path('bookadd/',       Book_Add.as_view(), name='bookadd_path'),

    # path('api/v1/auth/', include('rest_framework.urls')),
    path('api/v1/auth/',   include('djoser.urls')),
    path('api/v1/auth/',   include('djoser.urls.authtoken')),
    path('api/v1/auth/authenticate/', CustomObtainAuthToken.as_view()),
    path('api/v1/profile', UserProfileView.as_view()),
    path('api/v1/profile/search', UserProfileView.as_view()),

    path('api/v1/',        include(router.urls)),   
    path('api/v1/age/',    Age_rangeApi.as_view()),
    path('api/v1/ggl/<str:id>', BookByGglId.as_view()),

    path('api/v1/library/', LibraryCreateAPI.as_view()),
    path('api/v1/library/list', LibraryListAPI.as_view()),
    path('api/v1/library/search/', LibrarySeachBook.as_view()),
    # path('bookadd/',       Book_Add.as_view(), name='bookadd_path'),

    path('api/v1/messages', MessagesCreateAPI.as_view()), 
    path('api/v1/messages/list', MessagesListAPI.as_view()),
    path('api/v1/messages/search', MessagesSearch.as_view()),
    path('api/v1/messages/change', MessagesChange.as_view()),

    path('api/v1/rents/list', RentsListAPI.as_view()),
    path('api/v1/rents', RentsCreateAPI.as_view()),
    path('api/v1/rents/change/<int:id>/', RentsChangeAPI.as_view()),

]
