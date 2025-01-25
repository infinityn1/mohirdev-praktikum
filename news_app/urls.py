from django.urls import path
from .views import news_list, news_detail, homePageView, contactPageView, not404, singlePage, HomePageView, LocalNewsView, SportNewsView, XorijNewsView, TechnologyNewsView

urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    path('news/', news_list, name='all_news_list'),
    path("news/<slug:news>/", news_detail, name='news_detail_page'),
    path('contact-us/', contactPageView, name="contact_page"),
    path('error/', not404, name="404_page"),
    path('single_page/', singlePage, name='single_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('xorij/', XorijNewsView.as_view(), name='xorij_news_page'),
    path('texnologiya/', TechnologyNewsView.as_view(), name='texnologiya_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page')
]


