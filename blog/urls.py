from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostsListView.as_view(), name="blog-home"),
    path('new/', views.PostCreateView.as_view(), name="blog-create"),
    path('post/<slug>-<int:pk>/', views.PostDetailView.as_view(), name="blog-post"),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name="blog-post"),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name="blog-edit"),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name="blog-delete"),
    path('user/<str:username>/', views.UserPostsView.as_view(), name="blog-user"),
    path('about/', views.about, name="about-home"),
    path('comments/', views.comments, name="blog-comments"),
]
