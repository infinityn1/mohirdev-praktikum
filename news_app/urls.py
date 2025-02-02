from django.urls import path
from .views import news_list, news_detail, homePageView, contactPageView, not404, singlePage, HomePageView, LocalNewsView, SportNewsView, \
XorijNewsView, TechnologyNewsView, NewsUpdateView, NewsDeleteView, NewsCreateView, admin_page_view, SearchListView
    
urlpatterns = [
    path('', HomePageView.as_view(), name="home_page"),
    path('news/', news_list, name='all_news_list'),
    path("news/<slug:news>/", news_detail, name='news_detail_page'),
    path('news/create', NewsCreateView.as_view(), name='news_create'),
    path('news/<slug>/edit', NewsUpdateView.as_view(), name='news_update'),
    path('news/<slug>/delete', NewsDeleteView.as_view(), name='news_delete'),
    path('contact-us/', contactPageView, name="contact_page"),
    path('error/', not404, name="404_page"),
    path('single_page/', singlePage, name='single_page'),
    path('local/', LocalNewsView.as_view(), name='local_news_page'),
    path('xorij/', XorijNewsView.as_view(), name='xorij_news_page'),
    path('texnologiya/', TechnologyNewsView.as_view(), name='texnologiya_news_page'),
    path('sport/', SportNewsView.as_view(), name='sport_news_page'),
    path("adminpage/", admin_page_view, name="admin_page"),
    path("searchresult/", SearchListView.as_view(), name="search_result"),
]


