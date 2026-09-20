from django.urls import path

from . import views
from .views import NoteDetailView

urlpatterns = [
    path('', views.home, name='home'),
    path('note/<int:pk>/', NoteDetailView.as_view(), name='note-detail'),
    path('note/<int:pk>/delete/', views.note_delete, name='note-delete'),
]
