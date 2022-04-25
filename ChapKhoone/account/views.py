from django.conf import settings
from django.contrib.auth import login, views
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import pyotp
from django.core.mail import send_mail, BadHeaderError

from .models import Cart, CartItem, CategoryStamp, Profile, Service, Stamp, Wallet 
from .forms import ContactForm, CustomUserCreationForm, EvidencStampForm, LoginForm, VerifyForm, UserChangeForm
from django.http.response import HttpResponseRedirect
from django.views.generic import ListView, DetailView

from .utils import send_sms
from .backends import UserModel, UserNotVerified
from django.views.generic.edit import FormView
from django.contrib import messages
from django.views.generic.base import View, TemplateView
from django.views import generic
from django.utils.decorators import method_decorator
from django.db.models import Count









class LoginView(views.LoginView):


    form_class = LoginForm
    template_name = 'registeration/login.html'
    redirect_authenticated_user = True

    
    def get(self, request, *args, **kwargs):
        
        if 'phone' in self.request.session.keys():
            del self.request.session['phone']
        return super().get(self, request, *args, **kwargs)
    

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        try :
            login(self.request, form.get_user())
        except UserNotVerified:
            """ exception will handeled by middleware"""
            pass
        else:
            return HttpResponseRedirect(self.get_success_url())
        


class VerifyMixin:
    
    @property
    def get_user(self):
        try:
            user = UserModel.objects.get(phone=self.request.session['phone'])
            return user
        except UserModel.DoesNotExist:
            return 
        except KeyError:
            return

    @property
    def set_token(self):
        user = self.get_user
        time_otp = pyotp.TOTP(user.key, interval=300)
        time_otp = time_otp.now()
        return time_otp
    


   
        
class VerifyView(VerifyMixin, FormView):
    form_class = VerifyForm
    success_url = reverse_lazy('login-not-auth')
    template_name = 'registeration/verify.html'

    def get(self, request, *args, **kwargs):
        if self.get_user:
            return super().get(self, request, *args, **kwargs)
        else :
            return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        
        otp_code = str(request.POST.get('otp_code'))
        user = self.get_user
        
        if  user.authenticate(otp_code):
            user.is_verified = True
            user.save()
            messages.success(self.request,'شماره مبایل شما تایید شد')
            return super().post(self, request, *args, **kwargs)
        else :
            messages.warning(self.request,'کد تایید اشتباه است ')
            return self.form_invalid(self.form_class)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['phone']=self.request.session['phone']
        return context





class ResendVerifyView(VerifyMixin, View):
    
    def get(self, request, *args, **kwargs):
        if self.get_user:
            user = self.get_user
            phone = user.phone
            token = self.set_token
            
            # send_sms(receptor=phone, token=token)
            print('========== OTP:',token)
            
        return HttpResponseRedirect(reverse_lazy('verify'))






class RegisterView(generic.CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registeration/register.html'
    success_url = reverse_lazy('login-not-auth')
    
    
    
    
    
class NotpermissionOr404(TemplateView):

    template_name = "base/error-404.html"
    
    
class AboutUs(TemplateView):

    template_name = "base/about-us.html"
    
    
def contact_form(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = f'{form.cleaned_data["subject"]} ; Message from {form.cleaned_data["name"]}'
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            recipients = [settings.EMAIL_ADDRESS]
            try:
                send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            messages.success(request, 'نظر شما با موفقیت ارسال شد به زودی به شما پاسخ خواهیم داد ممنون از شما')
            return redirect('landing-home')
    return render(request, 'base/contant-us.html', {'form': form})



def Landing(request):
    form = ContactForm()
    services = Service.objects.all()
    
    if request.method == 'POST':
        print("-----------after post----------------")
        form = ContactForm(request.POST)
        print("---------------form-----:", form)
        if form.is_valid():
            subject = f'{form.cleaned_data["subject"]} ; Message from {form.cleaned_data["name"]}'
            message = form.cleaned_data["message"]
            sender = form.cleaned_data["email"]
            recipients = [settings.EMAIL_ADDRESS]
            try:
                send_mail(subject, message, sender, recipients, fail_silently=True)
            except BadHeaderError:
                return HttpResponse('Invalid header found')
            messages.success(request, 'نظر شما با موفقیت ارسال شد به زودی به شما پاسخ خواهیم داد ممنون از شما')
            return redirect('landing-home')
    return render(request, 'base/landing-home.html', {'form': form, 'service':services})



@login_required(login_url='login-not-auth')
def Dashboard(request):
    wallet = Wallet.objects.get(user=request.user)
    services = Service.objects.all()
    
    
    return render(request, 'base/dashboard.html', {'wallet': wallet, 'service':services})




@method_decorator(login_required, name='dispatch')
class UserEditView(generic.UpdateView):
    form_class = UserChangeForm
    template_name = 'base/profile.html'
    success_url = reverse_lazy('profile')
    success_message = "اطلاعات حساب کاربری به روز شد "

    def get_object(self):
        return self.request.user.profile
    
    
    
def search(request):

    if request.method == 'POST':
        searched = request.POST['searched']

        return render(request, 'search.html', {'searched': searched,})
    else:
        return render(request, 'search.html', )
    
    
    
    
def invite_code(request):
        code = request.POST['code']
        user = Profile.objects.get(invite_code=code)
        if user:
            wallet = Wallet.objects.get(user=user)
            cash = wallet.cash
            cash += 20000
            wallet.cash = cash
            wallet.save()
            user.use_invite_code = True
            user.save()
            messages.success(request, 'با تشکر از شما کد معهرف با موفقیت ثبت شد')
            
            
            
            
            
# @method_decorator(login_required, name='dispatch')
class StampList(ListView):
    template_name = "base/stamp-list.html"
    context_object_name = 'stamp'
    
    
    def get_queryset(self):
        return Stamp.objects.all()

    def get_context_data(self, **kwargs):
        context = super(StampList, self).get_context_data(**kwargs)
        context['user'] = self.request.user
        context['category'] = CategoryStamp.objects.all()
        return context
    
    
    
    
    
    
class StampByCategory(DetailView):
    model = CategoryStamp
    context_object_name = 'stamp'
    template_name = "base/stamp-category.html"

    def get_context_data(self, **kwargs):
        context = super(StampByCategory, self).get_context_data(**kwargs)
        context['category_all'] = CategoryStamp.objects.annotate(count_stamp=Count('stamp'))
        return context
    
    
    
    

def stamp_detail(request, slug):
    stamp = Stamp.objects.get(slug=slug)
    stamp_form = EvidencStampForm()
    
    if request.method == 'POST':
        print("------------after post--------")
        form = EvidencStampForm(request.POST, request.FILES)
        # form.save()
        print("------------form-save------------")
        
        print("---------form:", form)
        if form.is_valid():
            print("------------after isvalid--------")
            
            evid = form.save(commit=False)
            evid.stamp = stamp
            evid.user = request.user
            evid.save()
            have_pending_cart = len(Cart.objects.filter(user=request.user, status_payment='PND'))
            if int(have_pending_cart) >= 1:
                cart = Cart.objects.filter(user=request.user, status_payment='PND').first()
            else:
                cart = Cart.objects.create(user=request.user)
            item = CartItem.objects.create(items=stamp, cart=cart)
            return redirect('cart-detail', pk=request.user.pk) 
    return render(request, 'base/stamp-detail.html', {'stamp': stamp, 'form': stamp_form})









@method_decorator(login_required, name='dispatch')
class CartDetail(DetailView):
    model = Cart
    context_object_name = 'cart'
    template_name = "cart-detail.html"


    def get_context_data(self, **kwargs):
        context = super(CartDetail, self).get_context_data(**kwargs)
        context['items'] = CartItem.objects.filter(cart=self.object)
        return context


    def post(self, request, *args, **kwargs):
        item_id = request.POST['cart_id']
        item = CartItem.objects.get(pk=item_id)
        item.delete()
        cart = self.get_object()
        cart.save()
        messages.success(request,"آیتم مورد نظر از سبد خرید کاربر حذف شد")
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)