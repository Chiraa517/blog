from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.home, name='home'),
    path('category/<str:slug>', views.category, name='category'),
    path('seepost', views.seepost, name='seepost'),
    path('viewallpost', views.viewallpost, name='viewallpost'),
    path('signin', views.signin, name='signin'),
    path('signup', views.signup, name='signup'),
    path('signout', views.signout, name='signout'),
    # User profile
    path('dashboard', views.dashboard, name='dashboard'),
    path('addblog', views.addblog, name='addblog'),
    path('update_blog/<str:slug>', views.update_blog, name='update_blog'),
    path('update_blog/updated_blog_fields/<int:id>', views.updated_blog_fields, name='updated_blog_fields'),
    path('deleteBlog/<str:slug>', views.deleteBlog, name='deleteBlog'),
    path('readmore/<str:slug>', views.readmore, name='readmore'),
    path('usercategory/<str:slug>', views.usercategory, name='usercategory'),
    path('profile', views.profile, name='profile'),
]
