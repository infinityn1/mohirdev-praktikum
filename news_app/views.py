from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from .models import News, Category
from .forms import ContactForm, CommentForm
from django.http import HttpResponse
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from news_project.custom_permissions import OnlyLoddegSuperUser
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin



def news_list(request):
    news_list = News.published.filter(status=News.Status.Published)
    
    context = {
        "news_list":news_list
    }
    
    return render(request, "news/news_list.html", context=context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)

    context = {}
    # hintcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits
    
    comments = news.comments.filter(active=True)
    comment_count = comments.count()
    new_comment = None
    
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    
    
    context = {
        "news": news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'comment_count': comment_count,
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
        context['local_news_one'] = News.published.filter(category__name = "Mahalliy").order_by("-publish_time")[:5]
        context['xorij_xabarlari'] = News.published.filter(category__name = "Xorij").order_by("-publish_time")[:5]
        context['sport_xabarlari'] = News.published.filter(category__name = "Sport").order_by("-publish_time")[:5]
        context['texnologiya_xabarlari'] = News.published.filter(category__name = "Texnologiya").order_by("-publish_time")[:5]

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

    
    
class NewsUpdateView(OnlyLoddegSuperUser, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'category', 'status')
    template_name = 'crud/news_edit.html'
    

class NewsDeleteView(OnlyLoddegSuperUser, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')
    
    
class NewsCreateView(OnlyLoddegSuperUser, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title', 'slug', 'body', 'image', 'category', 'status')


@login_required
@user_passes_test(lambda u:u.is_superuser)
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    
    context = {
        "admin_users":admin_users
    }
    
    return render(request, 'pages/admin_page.html', context)


class SearchListView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query)
            
        )