from django.urls import path
from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, AddCategoryView, AddCommentView, category_view, category_list_view, like_view
from django.contrib.auth.decorators import login_required

app_name = 'myblog'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article-detail'),
    path('add_post/', login_required(AddPostView.as_view()), name='add-post'),
    path('add_category/', login_required(AddCategoryView.as_view()), name='add-category'),
    path('article/edit/<int:pk>/', login_required(UpdatePostView.as_view()), name='edit-post'),
    path('article/delete/<int:pk>/', login_required(DeletePostView.as_view()), name='delete-post'),
    path('category/<str:cats>/', category_view, name='category'),
    path('category-list/', category_list_view, name='category-list'),
    path('like/<int:pk>/', like_view, name='like-post'),
    path('article/<int:pk>/comment/', login_required(AddCommentView.as_view()), name='add-comment'),
]

