from django.contrib.staticfiles.urls import static
from django.contrib import admin
from django.urls import path, include
from . import settings
from account.views import AboutUs, CartDetail, StampByCategory, StampList, contact_form, search, Landing, LoginView, RegisterView, VerifyView, ResendVerifyView, NotpermissionOr404, stamp_detail








urlpatterns = [
                  path('grappelli/', include('grappelli.urls')),
                  path('admin/', admin.site.urls),
                  
                  path('acoounts/login/', LoginView.as_view(), name='login-not-auth'),
                  path('acoounts/verify-phone-number/', VerifyView.as_view(), name='verify'),
                  path('acoounts/verify-phone-number/resend/', ResendVerifyView.as_view(), name='resend'),
                  path('acoounts/register/', RegisterView.as_view(), name='register-not-auth'),

                  path('acoounts/', include('django.contrib.auth.urls')),
                  
        
                  path('error-404/', NotpermissionOr404.as_view(), name='not-permission'),
                  path('', Landing, name='landing-home'),
                  
                  path('dashboard/', include('account.urls')),
                  path('search/', search, name='search'),
                  path('about-us/', AboutUs.as_view(), name='about-us'),
                  path('contact-us/', contact_form, name='contact-us'),
                  path('stamp/', StampList.as_view(), name='stamp-list'),
                  path('stamp/<slug:slug>/', StampByCategory.as_view(), name='stamp-category'),
                  path('stamp-detail/<slug:slug>/', stamp_detail, name='stamp-detail'),
                  path('cart-detail/<int:pk>', CartDetail.as_view(), name='cart-detail')
                  
    

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
