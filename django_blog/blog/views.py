from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm  # For profile management
from django.contrib import messages
from django.views.generic import ListView , DetailView , CreateView ,UpdateView ,DeleteView
from .models import Post ,Comment
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# Registration View
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile View
@login_required
def profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})

# Logout View
from django.contrib.auth import logout
def logout_view(request):
    logout(request)
    return redirect('login')





class PostListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    
class PostCreateView(LoginRequiredMixin, UserPassesTestMixin,CreateView):
    model = Post
    template_name = 'blog/form.html'
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model = Post
    template_name = 'blog/form.html'
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'blog/form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'blog/form.html'
    
class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'blog/form.html'
    
class CommentListView(ListView):
    model = Comment
    template_name = 'blog/form.html'
    
class CommentCreateView(CreateView):
    model = Comment
    template_name = 'blog/form.html'
    
class CommentDetailView(DetailView):
    model = Comment
    template_name = 'blog/form.html'
    

def search_posts(request):
    query = request.GET.get('q', '')  # Get the search query from the GET parameters
    posts = Post.objects.all()

    if query:
        # Use Q objects to filter posts by title, content, or tags
        posts = posts.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(tags__name__icontains=query)  # Filter by tags (tags are linked via many-to-many relationship)
        ).distinct()  # Use distinct to avoid duplicate posts if they're tagged with the same keyword

    return render(request, 'search_results.html', {'posts': posts, 'query': query})