from django.urls import path

from .views import GameCreateView, GameDetailView, GameListView

urlpatterns = [
    path('', GameListView.as_view(), name='games_list'),
    path('create/', GameCreateView.as_view(), name='game_create'),   
    path('<slug:slug>/', GameDetailView.as_view(), name='game_detail'),
]