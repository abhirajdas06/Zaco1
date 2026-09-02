from django.views import generic
from .models import Post, Category
from django.db.models import Count



class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'blog.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['categories_list'] = Category.objects.all().annotate(posts_count=Count('post'))
          return context

class PostDetail(generic.DetailView):
    model = Post
    template_name = 'blog-single.html'
    
    
    def get_context_data(self, **kwargs):
          context = super().get_context_data(**kwargs)
          context['categories_list'] = Category.objects.all().annotate(posts_count=Count('post'))
          return context



