import json
from datetime import datetime

from django.conf import settings
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.views import View

from news.forms import ArticleForm


# Create your views here.

def get_articles():
    with open(settings.NEWS_JSON_PATH, "r") as json_file:
        article_list = json.load(json_file)
    for item in article_list:
        item["created"] = datetime.strptime(item["created"], "%Y-%m-%d %H:%M:%S")
    return article_list


def save_articles(article_list):
    for item in article_list:
        item["created"] = item["created"].strftime("%Y-%m-%d %H:%M:%S")
    with open(settings.NEWS_JSON_PATH, "w") as json_file:
        json.dump(article_list, json_file)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return redirect('news:article_list')


class ArticleView(View):
    def get(self, request, link):
        for article in get_articles():
            if article['link'] == link:
                context = {"article": article}
                return render(request, 'news/article.html', context)
        return HttpResponseNotFound("The item you are looking for does not exists!")


class ArticleListView(View):
    def get(self, request):
        q = request.GET.get("q")
        articles = get_articles()
        if not q:
            context = {'articles': articles}
            return render(request, 'news/article_list.html', context)
        else:
            articles_filtered = [article for article in articles if q in article["title"]]
            context = {'articles': articles_filtered}
            return render(request, 'news/article_list.html', context)


class ArticleCreateView(View):
    form_class = ArticleForm
    template_name = 'news/article_create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # form.save()  # till the database is created it will stay commented
            title = form.cleaned_data["title"]
            text = form.cleaned_data["text"]
            created = datetime.now()
            article_list = get_articles()
            article_list.append({"title": title, "text": text, "created": created})
            save_articles(article_list)
            return redirect('news:article_list')
        return render(request, self.template_name, {'form': form})
