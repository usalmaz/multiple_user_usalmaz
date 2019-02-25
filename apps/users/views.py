from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .forms import UserCreationModelForm
from .models import User, Post

class UserRegistrationView(CreateView):
    form_class = UserCreationModelForm
    success_url = reverse_lazy('login')
    template_name = 'users/registration.html'

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'country', 'city', 'address', 'email', 'phone', 'website']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'country', 'city', 'address', 'email', 'phone', 'website']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class CabinetView(LoginRequiredMixin, DetailView):
    model = User

    def get_object(self):
        return self.request.user

def blog(request):

    context = {
            'posts': Post.objects.filter(author=request.user)
    }
    return render(request, 'users/post_list.html', context)

def countries(request):

    user = User.objects.all()
    country = Post.objects.all().distinct('country')

    context = {
        'posts': country,
        'user': user
    }

    return render(request, 'users/countries.html', context)



def cities(request, pk):

    country = Post.objects.get(id=pk).country
    cities = Post.objects.filter(country=country).distinct('city')
    author = Post.objects.get(id=pk).author

    context = {
        'cities':cities,
        'country':country,
        'author':author,

    }

    return render(request, 'users/cities.html', context)

def address(request, pk):
    user = User.objects.all()
    city = Post.objects.get(id=pk).city
    address = Post.objects.filter(city=city)
    email = Post.objects.all()

    context = {
        'user': user,
        'address': address,
        'city': city,
    }

    return render(request, 'users/address.html', context)

def home(request):
        user = User.objects.all()
        country = Post.objects.all().distinct('country')

        context = {
            'posts': country,
            'user': user
        }

        return render(request, 'registration/home.html', context)
