from django.urls import path

from . import views
from . import api_views

app_name = 'blog'

urlpatterns = [
    # post views
    # path('', views.post_list, name='post_list'),
    path('', views.PostListView.as_view(), name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.post_detail, name='post_detail'),
    path('favrourite/add/<int:id>/', views.add_favourite, name='add_favourite'),
    path('favourites/', views.favourites, name='favourites'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('<int:post_id>/comment/', views.post_comment, name='post_comment'),

    # API endpoints
    path('api/', api_views.api_root, name='api_root'),
    path('api/posts/', api_views.PostListAPIView.as_view(), name='post_list_api'),
    path('api/posts/<int:pk>/', api_views.PostDetailAPIView.as_view(), name='post_detail_api'),
    path('api/posts/<int:post_id>/comments/', api_views.CommentListCreateAPIView.as_view(), name='comment_list_create_api'),
]
