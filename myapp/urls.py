# myapp/urls.py
from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from .views import UserProfileView, SearchUserView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
       path('home', home, name='home'),
    path('login', login_view, name='login'),
     path('admin_post/', admin_post, name='admin_post'),
    path('register', register, name='register'),  
     path('send_message/', send_message, name='send_message'),
      path('news', news, name='news'),
        path('jobs', jobs, name='jobs'),
          path('events', events, name='events'),
    path('logout', logout_view, name='logout'),
    path('post', post, name='post'),
    path('profile/', profile, name='profile'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('post_comment/<int:post_id>/', post_comment, name='post_comment'),
    path('user/<str:username>/', UserProfileView.as_view(), name='user_profile'),
 path('delete_comment/<int:comment_id>/', delete_comment, name='delete_comment'),
       path('get_comments/', get_comments, name='get_comments'),
    path('search/', SearchUserView.as_view(), name='search_user'),
     path('delete_message/<int:message_id>/', delete_message, name='delete_message'),
       path('send_message/<int:receiver_id>/', send_message, name='send_message'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)