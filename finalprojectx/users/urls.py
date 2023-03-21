from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #path('register/', views.registerUser, name='register'),
    #path('login/', views.LoginView.as_view(), name='login'),
    #path('logout/', views.logoutUser, name="logout"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerUser, name="register"),
    path('', views.index, name='index-view'),
    path('image/<str:pk>/', views.singleimages, name="image"),
    path('manager-image/<str:pk>/', views.managersingleimageview, name="managersingleimage"),
    path('account/', views.useraccount, name= 'account'),

    path('project/<str:pk>/', views.projectimages, name="project"),
    path('create-project/', views.createProject, name="create-project"),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),
    path('delete-project/<str:pk>/', views.deleteProject, name="delete-project"),
]


urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
