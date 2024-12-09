from django.urls import path
from authy.views import  Signup, PasswordChange, PasswordChangeDone,UserProfile,EditProfile,CustomLoginView

from django.contrib.auth import views as authViews 



urlpatterns = [
    path('profile/<str:username>/', UserProfile, name='profile'),
    path('profile/edit', EditProfile, name='edit-profile'),
   	path('signup/', Signup, name='signup'),
    path('login/', CustomLoginView.as_view(), name='login'),
   	path('logout/', authViews.LogoutView.as_view(), {'next_page' : 'home'}, name='logout'),
   	path('changepassword/', PasswordChange, name='change_password'),
   	path('changepassword/done', PasswordChangeDone, name='change_password_done'),
   	path('passwordreset/', authViews.PasswordResetView.as_view(), name='password_reset'),
   	path('passwordreset/done', authViews.PasswordResetDoneView.as_view(), name='password_reset_done'),
   	path('passwordreset/<uidb64>/<token>/', authViews.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
   	path('passwordreset/complete/', authViews.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


]