from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from .forms import RegisterForm, LoginForm, UpdateProfileForm, UpdateUserForm, CreateBlogForm, UpdateBlogForm, DeleteBlogForm
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .models import Blog
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home(request):
    return render(request, 'home.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'register.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, {'form': form})
    

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect(to='/')
        return render(request, self.template_name, {'form': form})
    

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True

        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)
    

def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)


@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'profile.html', {'user_form': user_form, 'profile_form': profile_form})


@login_required
def blogs(request):
    blogs = Blog.objects.all()
    return render(request, 'blogs.html', {
        'blogs': blogs
    })


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

# @login_required
class CreateBlogView(LoginRequiredMixin, View):
    form_class = CreateBlogForm
    initial = {'key': 'value'}
    template_name = 'blog-create.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            blog = form.save(commit=False)  # Create an instance without saving to the database yet
            blog.author = request.user  # Set the author to the logged-in user
            blog.save()
            title = form.cleaned_data.get('title')
            messages.success(request, f'Blog created: {title}')
            return redirect('blogs')
        return render(request, self.template_name, {'form': form})


# @login_required
class UpdateBlogView(LoginRequiredMixin, View):
    model = Blog
    form_class = UpdateBlogForm
    initial = {'key': 'value'}
    template_name = 'blog-update.html'
    def get(self, request, *args, **kwargs):
        blog_id = self.kwargs.get('blog_id')
        try:
            blog = Blog.objects.get(id=blog_id)
            form = self.form_class(initial = self.initial, instance=blog)
        except Blog.DoesNotExist:
            pass
        return render(request, self.template_name, {'form': form, 'blog': blog})

    def post(self, request, *args, **kwargs):
        blog_id = self.kwargs.get('blog_id')
        blog = Blog.objects.get(id=blog_id)
        form = self.form_class(request.POST, request.FILES, instance=blog)

        if form.is_valid():
            form.save()
            title=form.cleaned_data.get('title')
            messages.success(request, f'Blog Updated: {title}')
            return redirect('blogs')
        return render(request, self.template_name, {'form': form})
    
def delete_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    blog.delete()
    messages.success(request, f'Post Deleted: {blog.title}')
    return redirect('blogs')

