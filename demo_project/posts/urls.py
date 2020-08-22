from django.urls import path

from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.PostListView.as_view(), name='index'),
    path('<int:pk>/', views.PostUpdateView.as_view(), name='update'),
]
