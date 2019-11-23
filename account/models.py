import stripe
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.db.models.signals import post_save
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY


class User(AbstractUser):
    is_innovator = models.BooleanField(default=False)
    is_investor = models.BooleanField(default=False)
    is_entrepreneur = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_service_provider = models.BooleanField(default=False)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    address = models.CharField(max_length=50, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    profile_image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True)
    profession = models.CharField(max_length=250, blank=True)
    street = models.CharField(max_length=250, blank=True)
    town = models.CharField(max_length=250, blank=True)
    zip_code = models.IntegerField(null=True)
    country = models.CharField(max_length=250, blank=True)
    phone_number = models.CharField(blank=True, max_length=13)
    bio = models.TextField(blank=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return 'Profile for user {}'.format(self.user)

    def get_absolute_url(self):
        return reverse('account:profile_detail', args=[self.id])


class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_chats')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1000)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'chat between {} and {} '.format(self.sender, self.receiver)


class Verification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verify_user')
    document_type = models.CharField(max_length=200)
    document = models.FileField(upload_to='Files/Verification/%Y/%m/%d')

    def __str__(self):
        return 'Verification docs for {}'.format(self.user)


class BusinessManagement(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.PositiveIntegerField()
    message = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name


class PlanCategories(models.Model):
    name = models.CharField(max_length=200)
    default_price_per_month = models.FloatField(null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portal:plan_cat', args=[self.id])


class Plans(models.Model):
    plan_category = models.ForeignKey(PlanCategories, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    stripe_plan_id = models.CharField(max_length=40, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.plan_category.name


class UserSubscriptions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plans, on_delete=models.SET_NULL, null=True)
    stripe_customer_id = models.CharField(max_length=50, null=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} has plan {}'.format(self.user, self.plan)


def post_save_user_subscription(sender, instance, created, *args, **kwargs):
    if created:
        UserSubscriptions.objects.get_or_create(user=instance)
    user_subscription, created = UserSubscriptions.objects.get_or_create(user=instance)

    if user_subscription:
        if user_subscription.stripe_customer_id is None or user_subscription.stripe_customer_id == '':
            new_customer_id = stripe.Customer.create(email=instance.email)
            user_subscription.stripe_customer_id = new_customer_id['id']
            user_subscription.plan = Plans.objects.get(name='Free')
            user_subscription.save()
            subscription = stripe.Subscription.create(
                customer=new_customer_id,
                items=[
                    {"plan": "plan_GAmCBtTCVEYk1T"},
                ],
            )
            Subscriptions.objects.create(user_subscription=user_subscription, stripe_subscription_id=subscription.id,
                                         active=True)


post_save.connect(post_save_user_subscription, User)


class Subscriptions(models.Model):
    user_subscription = models.ForeignKey(UserSubscriptions, on_delete=models.CASCADE)
    stripe_subscription_id = models.CharField(max_length=50)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_subscription.user.username








