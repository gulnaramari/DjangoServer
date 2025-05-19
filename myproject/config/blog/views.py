from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post

class PostsListView(ListView):
    model = Post
    template_name = 'blog/goodbye.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """ Выводим только опубликованные статьи """
        return Post.objects.filter(is_published=True)


class PostDetailsView(DetailView):
    model = Post
    template_name = 'blog/post_details.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """ Увеличиваем количество просмотров при каждом открытии статьи """
        post = super().get_object(queryset)
        post.views += 1
        post.save(update_fields=['views'])
        return post


class PostCreateView(CreateView):
    model = Post
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blog/add_post.html'
    success_url = reverse_lazy('blog:home')


class PostUpdateView(UpdateView):
    model = Post
    fields = ['title', 'content', 'image', 'is_published']
    template_name = 'blog/add_post.html'

    def get_success_url(self):
        return reverse('blog:post_details', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog:home')
