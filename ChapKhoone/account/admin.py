from __future__ import unicode_literals
from django.contrib.auth import get_user_model
from django.contrib import admin
User = get_user_model()

from .forms import CustomUserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Cart, CartItem, CategoryStamp, Country, City, EssenceStamp, EvidenceStamp, Profile, CustomUser, Service, ShapeStamp, Stamp, Transaction, Wallet




class CustomUserAdmin(BaseUserAdmin):

    add_form = CustomUserCreationForm
    model = User
    list_display = ('username','email','phone', 'is_staff', 'is_active','is_verified',)
    list_filter = ('username','email','phone','is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password',),}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_verified',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email','phone', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('phone', 'username')
    ordering = ('phone', 'username')

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'sexuality', 'age','description', 'address', 'city')
    list_filter = ('sexuality',)
    search_fields = ('age', 'city')



    
    
    


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(City)
admin.site.register(Country)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Stamp)
admin.site.register(EvidenceStamp)
admin.site.register(ShapeStamp)
admin.site.register(EssenceStamp)
admin.site.register(CategoryStamp)
admin.site.register(Service)






