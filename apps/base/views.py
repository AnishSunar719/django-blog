from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth.views import LoginView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

from django.urls import reverse_lazy

from .models import Blog

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name='register/login.html'
    def get_success_url(self):
        return reverse_lazy("base:home")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Login'
        return context    

class RegisterView(FormView):
    template_name = 'register/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy("base:home")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Register'
        return context
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('base:home')
        return super(RegisterView, self).get(*args, **kwargs)

class HomePage(ListView):
    template_name = 'base/home.html'
    context_object_name = 'blogs'
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q')
        context['title'] = 'Home'
        if q:
            context['blogs'] = Blog.objects.filter(title__icontains=q) or Blog.objects.filter(user__username__icontains=q)
        else:
            context['blogs'] = Blog.objects.all()
        return context

class DetailPage(DetailView):
    template_name = 'base/detail.html'
    context_object_name = 'blog'
    model = Blog
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        context["title"] = blog.title
        return context
    

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    fields = ['title', 'image', 'description']
    template_name="base/form.html"
    success_url = reverse_lazy("base:home")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(BlogCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Create Blog'
        return context
    
class UserBlogsView(LoginRequiredMixin, ListView):
    model = Blog
    template_name='base/home.html'
    context_object_name = "blogs"
    
    def get_queryset(self):
        return Blog.objects.filter(user = self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Blogs'
        return context

class BlogEditView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    template_name = 'base/form.html'
    model = Blog
    fields = ['title', 'image', 'description']
    def get_success_url(self):
        return reverse_lazy('base:home')

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.user or self.request.user.is_superuser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Blog'
        return context

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'base/delete_confirm.html'
    model = Blog
    success_url = reverse_lazy('base:home')
    context_object_name = 'blog'

    def test_func(self):
        blog = self.get_object()
        return self.request.user == blog.user or self.request.user.is_superuser
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Delete Blog'
        return context