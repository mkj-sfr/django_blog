from django.urls import path
from .views import home, RegisterView, CustomLoginView, profile, ChangePasswordView, CreateBlogView, UpdateBlogView, blogs, delete_blog
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='users-home'),
    path('register', RegisterView.as_view(), name='users-register'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='login.html',authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profile/', profile, name='users-profile'),
    path('blogs/', blogs, name='blogs'),
    path('password-change/', ChangePasswordView.as_view(), name='change_password'),
    path('create-blog/', CreateBlogView.as_view(), name='create-blog'),
    path('update-blog/<int:blog_id>/', UpdateBlogView.as_view(), name='update-blog'),
    path('delete-blog/<int:blog_id>/', delete_blog, name="delete-blog"),



] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)