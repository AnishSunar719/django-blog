from django.urls import path

from apps.base.views import HomePage, DetailPage, BlogCreateView, UserBlogsView, BlogEditView, BlogDeleteView

app_name='base'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('blog/<str:user>/<int:id>/<slug:slug>', DetailPage.as_view(), name='detail-page'),
    path('create-blog/', BlogCreateView.as_view(), name='create-blog'),
    path('<str:user>/', UserBlogsView.as_view(), name='user-blogs'),
    path('edit/<str:usr>/<int:id>/<slug:slug>', BlogEditView.as_view(), name='edit-blog'),
    path('delete/<str:user>/<int:id>/<slug:slug>', BlogDeleteView.as_view(), name='delete-blog')
    
]
