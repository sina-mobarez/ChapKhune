from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, ReadOnlyPasswordHashField
from .models import CustomUser, EvidenceStamp, Profile



class CustomUserCreationForm(UserCreationForm):

    class Meta:
            model = CustomUser
            fields = ('email', 'username', 'phone', 'password1', 'password2')
            
            widgets = {
                'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'نام کاربر'}),
                'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'ایمیل'}),
                'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'نام کاربری'}),
                'password1': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'رمز عبور'}), 
                'password2': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'تکرار رمز عبور'}),
            }




class LoginForm(AuthenticationForm):
    
    username = forms.CharField(label="نام کاربری/شماره همراه/ایمیل",widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder':'نام کاربری/شماره همراه/ایمیل'}))
    
    
    
    
class VerifyForm(forms.Form):
    
    otp_code = forms.CharField(label='کد تایید', max_length=6, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد تایید'}),
                        error_messages = {
                            'required' : 'این فیلد الزامی میباشد',
                            'max_length' : 'کاراکتر بیش از حد مجاز '
                        }
    
                    )
    
    
    
    
class ContactForm(forms.Form):
    name = forms.CharField(max_length=80, label='نام و نام خانوادگی')
    subject = forms.CharField(max_length=80, label='عنوان')
    message = forms.CharField(widget=forms.Textarea, label='پیام')
    email = forms.EmailField(label='ایمیل')
    
    
    
    
    
class UserChangeForm(UserChangeForm):
    password = ReadOnlyPasswordHashField(label='رمز ورود',
                                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'نام کاربر'}),
        help_text=(
            '.متاسفانه قادر به نمایش رمز عبور شما نیستیم'
            'ولی برای تغییر ان میتواید از.'
            '<a href="{}">این لینک</a>.'
            'استفاده کنید'
            
        ),
    )

    class Meta:
        model = Profile
        fields = ('description', 'first_name', 'last_name', 'address', 'age', 'sexuality', 'image', 'city', 'password')





class EvidencStampForm(forms.ModelForm):

    class Meta:
        model = EvidenceStamp
        fields = ['evidence', 'evidence2', 'sketch_stamp', 'note', 'is_framework']