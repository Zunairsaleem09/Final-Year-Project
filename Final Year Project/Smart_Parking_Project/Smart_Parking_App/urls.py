from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('base',views.base,name='base'),
    path('whyus',views.whyus,name='why'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('',views.parkhome,name='parkhome'),
    path('home',views.home,name='home'),
    path('signup',views.signup,name='signup'),
    path('login',views.login_user,name='login'),
    path('token_send',views.token_send,name="token_send"),
    path('success',views.success,name='success'),
    path('verify/<auth_token>',views.verify,name="verify"),
    path('error',views.error_page,name="error"),
    path('logout/',views.logout_user, name='logout'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="reset_password.html"), name='reset_password' ),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="reset_password_sent.html"), name='password_reset_done'),
    path('reset<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
    path('admin/',admin.site.urls),
    path('garage',views.garage,name="garage"),
    path('garagehome',views.garage_home,name="garagehome"),
    path('profile',views.garage_profile,name="profile"),
    #Post Related URLS
    path("posts", views.post_index, name="post"),
    path("navbar", views.navbar, name="navbar"),
    path("create_project", views.create_product, name='uploadpost'),
    path("post/<str:id>", views.detail, name ='detail_page'),
    path("myadd", views.myadd, name="myadd"),
    path("parkbase/<int:pk>/", views.reserve_parking, name="parkbase"),
    path("booking", views.search, name="search"),
    path('pdf/',views.pdf,name='pdf'),
    # path('buy/<int:pk>/',views.buy,name='buy'),
    # path('invoice/',views.pdf,name='invoice'),
    path('send/', views.send_chat, name='chat-send'),
    path('renew/', views.get_messages, name='chat-renew'),
    path('chat', views.chat_home, name='index'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)