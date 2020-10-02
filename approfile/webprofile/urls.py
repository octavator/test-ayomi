from django.urls import path

from . import views

app_name = 'webprofile'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('inscription', views.RegisterFormView.as_view(), name='register'),
    path('vue', views.UserView.as_view(), name='userView'),
    path('edition', views.UserView.as_view(), name='userView'),
    path('logout', views.logout, name='logout'),    

    #path('edition', views.editProfile, name='editProfil'),
    ]