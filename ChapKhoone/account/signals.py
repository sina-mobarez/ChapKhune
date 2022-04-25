from .models import CustomUser, Profile, Wallet
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
import pyotp
from django.utils.crypto import get_random_string



@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        invite_code = str(instance.id) + get_random_string(length=6)
        Profile.objects.create(user=instance, invite_code=invite_code)
        
        
        
@receiver(post_save, sender=CustomUser)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance)

        
        
def generate_key():
    """ User otp key generator """
    key = pyotp.random_base32()
    if is_unique(key):
        return key
    generate_key()
    
    

def is_unique(key):
    try:
        CustomUser.objects.get(key=key)
    except CustomUser.DoesNotExist:
        return True
    return False



@receiver(pre_save, sender=CustomUser)
def create_key(sender, instance, **kwargs):

    if not instance.key:
        instance.key = generate_key()