from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Feed and main pages
    path('', views.feed_view, name='feed'),
    path('analytics/', views.analytics_view, name='analytics'),
    path('analytics/data/', views.analytics_data_view, name='analytics_data'),
    
    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Post management
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post_view, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post_view, name='delete_post'),
    path('post/<int:pk>/like/', views.toggle_like_view, name='toggle_like'),
    path('post/<int:pk>/comment/', views.add_comment_view, name='add_comment'),
    
    # Profile
    path('profile/<str:username>/', views.profile_view, name='profile'),
]