from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.core import mail
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from .forms import UserCreationModelForm, UserUpdateForm, ProfileUpdateForm
from .models import User, Post, Profile, Country

class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserCreationModelForm
    model = User
    success_url = reverse_lazy('login')
    success_message = "Account for %(first_name)s was created successfully. You will get email notification when admin will activate your account!"
    template_name = 'users/registration.html'

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(cleaned_data)


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

@login_required
def cabinet(request):
    profile = Profile.objects.all()

    context = {
        'profile': profile

    }
    return render(request, 'users/user_detail.html', context)


@login_required
def profile(request):
    if request.method == 'POST':
        uform = UserUpdateForm(request.POST, instance=request.user)
        pform = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        posts = Post.objects.filter(author=request.user)

        if uform.is_valid() and pform.is_valid():
            uform.save()
            pform.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('users:cabinet')
    else:
        uform = UserUpdateForm(instance=request.user)
        pform = ProfileUpdateForm(instance=request.user.profile)
        posts = Post.objects.filter(author=request.user)

    context = {
        'uform': uform,
        'pform': pform,
        'posts': posts
    }

    return render(request, 'users/user_detail.html', context)

@login_required
def blog(request):

    context = {
            'posts': Post.objects.filter(author=request.user)
    }
    return render(request, 'users/post_list.html', context)


def countries(request):

    user = User.objects.all()
    country = Post.objects.all().order_by('country').distinct('country')

    context = {
        'posts': country,
        'user': user
    }

    return render(request, 'users/countries.html', context)



def cities(request, pk):
    country = Post.objects.get(id=pk).country
    cities = Post.objects.filter(country=country).distinct('city')
    author = Post.objects.get(id=pk).author
    access_challenge_country = Country.objects.filter(access_challenge = True)

    context = {
        'cities':cities,
        'country':country,
        'author':author,
        'access_challenge_country': access_challenge_country

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
        cname = request.POST.get('dropdown1')
        city = Post.objects.all().distinct('city')
        country = Post.objects.all().distinct('country').order_by('country_id')


        context = {
            'country': country,
            'user': user,
            'city': city
        }

        return render(request, 'registration/home.html', context)
