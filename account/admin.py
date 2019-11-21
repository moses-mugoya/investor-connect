from django.contrib import admin
from .models import Profile, User, Chat, Verification, BusinessManagement, UserSubscriptions, Plans,\
    PlanCategories, Subscriptions
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserRegistrationForm, UserEditForm
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail


class UserAdmin(BaseUserAdmin):
    add_form_template = 'admin/auth/user/add_form.html'
    change_user_password_template = None
    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'first_name', 'last_name', 'is_innovator', 'is_investor', 'is_entrepreneur', 'is_verified')}
         ),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'password2')
        }),
    )
    list_filter = ['is_innovator', 'is_investor', 'is_entrepreneur', 'is_superuser', 'is_verified']
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_verified']

    form = UserEditForm
    add_form = UserRegistrationForm


admin.site.register(User, UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


admin.site.register(Profile, ProfileAdmin)


class ChatAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'created', 'modified', 'message']
    list_filter = ['created', 'sender', 'receiver']
    search_fields = ['message']


admin.site.register(Chat, ChatAdmin)


class VerificationAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        qs = Verification.objects.filter(user__is_verified=False)
        return qs

    def approve(self, request, queryset):
        for query in queryset:
            user = get_object_or_404(Profile, user=query.user)
            user.user.is_verified = True
            user.user.save()
            user_email = user.user.email
            sender = 'centinum@gmail.com'
            message = "Hi {}, your profile has been approved please login to" \
                      " Centinum to access our services".format(user.user.username)
            subject = 'Profile Approved'
            send_mail(subject, message, sender, [user_email])
            self.message_user(request, "Profile for {} Has Been Approved successfully.".format(user.user.username))

    approve.short_description = 'Approve Profile'

    def decline(self, request, queryset):
        for query in queryset:
            user = get_object_or_404(Profile, user=query.user)
            user_email = user.user.email
            sender = 'centinum@gmail.com'
            message = "Hi {}, your profile has been declined. We are very sorry".format(user.user.username)
            subject = 'Profile Declined'
            send_mail(subject, message, sender, [user_email])
            self.message_user(request, "Profile for {} Has Been Declined successfully.".format(user.user.username))

    decline.short_description = 'Decline Profile'

    list_display = ['document_type', 'user', 'document']
    list_filter = ['user', 'document_type']
    actions = [approve, decline]


admin.site.register(Verification, VerificationAdmin)


class BusinessAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'message', 'created']
    list_display_links = ['first_name']


admin.site.register(BusinessManagement, BusinessAdmin)


class PlanCategoriesAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'default_price_per_month']


admin.site.register(PlanCategories, PlanCategoriesAdmin)


class PlansAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'stripe_plan_id', 'price',  'plan_category', 'created']


admin.site.register(Plans, PlansAdmin)


class UserSubAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'created', 'modified', 'stripe_customer_id']


admin.site.register(UserSubscriptions, UserSubAdmin)


class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ['user_subscription', 'stripe_subscription_id', 'active']


admin.site.register(Subscriptions, SubscriptionsAdmin)


admin.site.site_header = "Centinum Group Backend"
admin.site.site_title = "Centinum Admin Portal"
admin.site.index_title = "Welcome to Centinum Admin Portal"



