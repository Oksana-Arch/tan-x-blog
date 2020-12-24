from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *

# app_name = 'blog'
urlpatterns = [
    path('', post_list, name='post_list_url'),
    path('page404/', error404_test, name = 'error404'),
    path('markdown/', markdown, name = 'markdown'),
    path('post/create/', PostCreate.as_view(), name = 'post_create_url'),
    path('post/<str:slug>/', post_detail, name = 'post_detail_url'),
    path('post/<str:slug>/update/', PostUpdate.as_view(), name = 'post_update_url'),
    path('post/<str:slug>/delete', PostDelete.as_view(), name = 'post_delete_url'),
    path('tags/', tag_list, name = 'tags_list_url'),
    path('tag/create/', TagCreate.as_view(), name = 'tag_create_url'),
    path('tag/<str:slug>/', TagDetail.as_view(), name = 'tag_detail_url'),
    path('tag/<str:slug>/update/', TagUpdate.as_view(), name = 'tag_update_url'),
    path('tag/<str:slug>/delete/', TagDelete.as_view(), name = 'tag_delete_url'),
    path('categories/', categ_list, name = 'categories_list_url'),
    path('category/create/', CategoryCreate.as_view(), name='category_create_url'),
    path('category/<str:slug>/', CategoryDetail.as_view(), name = 'category_detail_url'),
    path('category/<str:slug>/update/', CategoryUpdate.as_view(), name = 'category_update_url'),
    path('category/<str:slug>/delete/', CategoryDelete.as_view(), name = 'category_delete_url'),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('search/', post_search, name = 'post_search'),
    path('contacts/', contact, name = 'contact'),
    path('thanks/', thanks, name = 'thanks'),
    path('arcive/', archive, name = 'archive'),
]