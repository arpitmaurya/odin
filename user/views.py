from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, RedirectView, DetailView, UpdateView
from .forms import *
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from user.models import User
from datetime import datetime
from django.conf import settings
from django.contrib.auth import get_user_model

User = settings.AUTH_USER_MODEL

class RegisterView(CreateView):
    model = settings.AUTH_USER_MODEL
    form_class = UserRegistrationForm
    template_name = 'user/register.html'
    success_url = 'login'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        return self.success_url

    def post(self, request, *args, **kwargs):
        if User.objects.filter(email=request.POST['email']).exists():
            messages.warning(request, 'This email already exists')
            return redirect('register')

        user_form = UserRegistrationForm(data=request.POST)

        if user_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            print(user_form.errors)
            return render(request, 'user/register.html', {'form': user_form})


class LoginView(FormView):
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'user/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = reverse_lazy('login')

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)





class TimelineView(DetailView):
    model = User
    template_name = "user/user-profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"
    context_object_name = "user"
    object = None

    def get_object(self, queryset=None):
        return self.model.objects.select_related('posts').prefetch_related("posts").get(
            username=self.kwargs.get(self.slug_url_kwarg))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)



class ProfileEditView(UpdateView):
    model = User
    template_name = "user/edit-my-profile.html"
    context_object_name = "user"
    object = None
    fields = "__all__"

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        print(request.POST.get('first_name'))
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.bio = request.POST.get('bio')
        if request.POST.get('gender') == 'M':
            user.gender = "Male"
        elif request.POST.get('gender') == "F":
            user.gender = "Female"
        else:
            user.gender = "Other"
        user.save()
        return redirect(reverse_lazy('edit-profile'))









@receiver(user_logged_in)
def got_online(sender, user, request, **kwargs):
    user.is_online = True
    user.save()

@receiver(user_logged_out)
def got_offline(sender, user, request, **kwargs):
    user.is_online = False
    user.last_seen = datetime.now()
    user.save()