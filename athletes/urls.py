from django.views.decorators.cache import cache_page
from django.urls import path
from athletes.views import *

urlpatterns = [
    path('', AthletesHome.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('addpage/', AthletesAddPage.as_view(), name='add_page'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('post/<slug:post_slug>', AthletesShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>', AthletesShowCategory.as_view(), name='category'),
]
