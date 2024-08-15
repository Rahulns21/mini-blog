from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect

class HomeView(ListView):
    model = Post
    template_name = 'home.html'
    ordering = ['-created_at']

    def get_context_data(self, *args, **kwargs):
        category_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["category_menu"] = category_menu
        return context

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        category_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

        post = get_object_or_404(Post, id=self.kwargs['pk'])
        total_likes = post.total_likes()

        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        context["category_menu"] = category_menu
        context["total_likes"] = total_likes
        context["liked"] = liked
        return context

class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('myblog:home') 

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Pass the logged-in user to the form
        return kwargs

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        # Fetch the post using the pk from the URL and assign it to the comment
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.post = post  # Set the post field of the Comment instance
        form.instance.name = self.request.user  # Assign the current logged-in user to the name field
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])  # Ensure the post is in the context
        return context
    
    def get_success_url(self):
        # Redirect to the article detail page after the comment is successfully added
        return reverse_lazy('myblog:article-detail', args=[str(self.object.post.pk)])

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'

    def form_valid(self, form):
        form.instance.name = form.instance.name.lower()
        return super().form_valid(form)

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'edit_post.html'

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('myblog:home')

def category_view(request, cats):
    category = get_object_or_404(Category, name=cats.replace('-', ' '))
    category_posts = Post.objects.filter(category=category)
    category_menu = Category.objects.all()
    context = {
        'category_posts': category_posts,
        'cats': cats.replace('-', ' '),
        'category_menu': category_menu,
    }
    return render(request, 'categories.html', context=context)

def category_list_view(request):
    category_menu_list = Category.objects.all()
    context = {
        'category_menu_list': category_menu_list
    }
    return render(request, 'category_list.html', context=context)

def like_view(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('myblog:article-detail', args=[str(pk)]))