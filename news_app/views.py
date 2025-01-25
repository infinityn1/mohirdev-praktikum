from django.shortcuts import render, get_object_or_404
from .models import News, Category
from .forms import ContactForm
from django.http import HttpResponse
from django.views.generic import ListView


def news_list(request):
    news_list = News.published.filter(status=News.Status.Published)
    
    context = {
        "news_list":news_list
    }
    
    return render(request, "news/news_list.html", context=context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        "news": news 
    }
    
    return render(request, "news/news_detail.html", context)


def homePageView(request):
    news_list = News.published.all().order_by("-publish_time")[:5]
    categories = Category.objects.all()
    local_news = News.published.all().filter(category__name = "Mahalliy")[1:6]
    local_news_one = News.published.filter(category__name = "Mahalliy").order_by("publish_time")[:1]
    
    context = {
        'news_list': news_list,
        "categories":categories,
        "local_news":local_news,
        "local_news_one":local_news_one
    }
    
    return render(request, "news/home.html", context)


class HomePageView(ListView):
    model = News
    template_name = 'news/home.html'
    context_object_name = 'news'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by("-publish_time")[:4]
        context['local_news_one'] = News.published.filter(category__name = "Mahalliy").order_by("publish_time")[:5]
        context['xorij_xabarlari'] = News.published.filter(category__name = "Xorij").order_by("publish_time")[:5]
        context['sport_xabarlari'] = News.published.filter(category__name = "Sport").order_by("publish_time")[:5]
        context['texnologiya_xabarlari'] = News.published.filter(category__name = "Texnologiya").order_by("publish_time")[:5]

        return context
    
    

def contactPageView(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return HttpResponse("Biz bilan boglanganingiz uchun tashakkur")
    context = {
        "form":form
    }
    
    return render(request, "news/contact.html", context)

def not404(request):
    
    return render(request, "news/404.html")

def singlePage(request):
    
    return render(request, 'news/single_page.html')


class LocalNewsView(ListView):
    model =  News
    template_name = 'news/mahalliy.html'
    context_object_name = 'mahalliy_yangiliklar'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news

    
class XorijNewsView(ListView):
    model =  News
    template_name = 'news/xorij.html'
    context_object_name = 'xorij_yangiliklar'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news

    
class TechnologyNewsView(ListView):
    model =  News
    template_name = 'news/texnologiya.html'
    context_object_name = 'texnologiya_yangiliklar'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news

    
    
class SportNewsView(ListView):
    model =  News
    template_name = 'news/sport.html'
    context_object_name = 'sport_yangiliklar'
    
    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news

    