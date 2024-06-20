# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.topic_list, name='index'),
    path('topics/', views.topic_list, name='topic_list'),
    path('topic/create/', views.topic_create, name='topic_create'),
    path('topic/<int:topic_id>/', views.topic_detail, name='topic_detail'),
    path('topic/<int:topic_id>/entry/create/', views.entry_create, name='entry_create'),
    path('entry/<int:entry_id>/edit/', views.edit_entry, name='edit_entry'),
    path("entry/<int:pk>/update", views.EntryUpdateView.as_view(), name="entry_update"),
    path('entry/delete/', views.delete_entry, name='entry_delete'),
    path("entry/<int:pk>", views.EntryDetailView.as_view(), name="entry_detail"),
    path('statistics/', views.entry_statistics, name='entry_statistics'),
    path('topic/delete/', views.delete_topic, name='topic_delete'),
    path('logout/', views.logout_view, name='logout'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('entry/<int:entry_id>/content/', views.entry_content, name='entry_content'),

]
