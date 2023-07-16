from django.urls import path
from news.views import ArticleView, ArticleListView, ArticleCreateView

app_name = 'news'

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list'),
    path('<int:link>/', ArticleView.as_view(), name="article"),
    path('create/', ArticleCreateView.as_view(), name="create_article"),
]
