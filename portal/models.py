from django.db import models
from account.models import User
from django.urls import reverse
from djrichtextfield.models import RichTextField


class Ideas(models.Model):
    user = models.ForeignKey(User, related_name='user_ideas', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    description = models.TextField()
    interest = models.CharField(max_length=50, null=True)
    patent_number = models.PositiveIntegerField(blank=True, null=True)
    copyright_number = models.PositiveIntegerField(blank=True, null=True)
    users_like = models.ManyToManyField(User,
                                        related_name='ideas_liked',
                                        blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Ideas'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portal:idea_detail', args=[self.id])

    def day_created(self):
        return self.created.strftime('%d')

    def month_created(self):
        return self.created.strftime('%b')


class StartupBusiness(models.Model):
    user = models.ForeignKey(User, related_name='user_startup', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=250)
    company_registration_number = models.IntegerField()
    founding_date = models.DateField()
    slogan = models.CharField(blank=True, max_length=250)
    pitch = models.TextField(blank=True)
    pitch_video_url = models.URLField(blank=True)
    customer_model = models.CharField(max_length=250)
    stake_you_are_giving_up = models.PositiveIntegerField(null=True)
    minimum_financing = models.DecimalField(max_digits=10, decimal_places=2)
    financing_you_are_looking_for = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=250)
    full_address = models.CharField(max_length=250)
    stage = models.CharField(max_length=250)
    sector = models.CharField(max_length=250)
    interest = models.CharField(max_length=50)
    users_like = models.ManyToManyField(User,
                                        related_name='business_liked',
                                        blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Startup Businesses'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('portal:business_detail', args=[self.id])

    def day_created(self):
        return self.created.strftime('%d')

    def month_created(self):
        return self.created.strftime('%b')


class BusinessImages(models.Model):
    business = models.ForeignKey(StartupBusiness, on_delete=models.CASCADE, related_name='business_images')
    image = models.ImageField(upload_to='images/business/%Y/%m/%d')

    def __str__(self):
        return 'Images for {}'.format(self.business)

    class Meta:
        verbose_name_plural = "Business Images"


class IdeaInvestments(models.Model):
    idea = models.ForeignKey(Ideas, related_name='invest_idea', on_delete=models.CASCADE)
    investor = models.ForeignKey(User, related_name='user_idea', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Idea Investments'

    def __str__(self):
        return 'Investment on {}'.format(self.idea)

    def day_created(self):
        return self.created.strftime('%d')

    def month_created(self):
        return self.created.strftime('%b')


class BusinessInvestments(models.Model):
    business = models.ForeignKey(StartupBusiness, related_name='invest_business', on_delete=models.CASCADE)
    investor = models.ForeignKey(User, related_name='user_business', on_delete=models.CASCADE)
    investor_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Business Investments'

    def __str__(self):
        return 'Investment on {}'.format(self.business)

    def day_created(self):
        return self.created.strftime('%d')

    def month_created(self):
        return self.created.strftime('%b')


class BusinessTeams(models.Model):
    business = models.ForeignKey(StartupBusiness, related_name='team_business', on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name='member_business', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Business Teams'

    def __str__(self):
        return 'Joined Team for {}'.format(self.business)

    def day_created(self):
        return self.created.strftime('%d')

    def month_created(self):
        return self.created.strftime('%b')


class IdeaTeams(models.Model):
    idea = models.ForeignKey(Ideas, related_name='team_idea', on_delete=models.CASCADE)
    member = models.ForeignKey(User, related_name='member_idea', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)
        verbose_name_plural = 'Idea Teams'

    def __str__(self):
        return 'Joined team for {}'.format(self.idea)

    def day_created(self):
        return self.created.strftime('%d')

    def month_created(self):
        return self.created.strftime('%b')


class CentinumVentures(models.Model):
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    company_name = models.CharField(max_length=250)
    company_registration_number = models.IntegerField()
    founding_date = models.DateField()
    slogan = models.CharField(max_length=250)
    pitch = models.TextField()
    pitch_video_url = models.URLField()
    customer_model = models.CharField(max_length=250)
    percentage = models.PositiveIntegerField(null=True)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    country = models.CharField(max_length=250)
    full_address = models.CharField(max_length=250)
    stage = models.CharField(max_length=250)
    sector = models.CharField(max_length=250)
    interest = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = 'Centinum Ventures'

    def __str__(self):
        return self.name


class GroupChats(models.Model):
    business = models.ForeignKey(StartupBusiness, related_name='group_chats', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=1000)
    user = models.ForeignKey(User, related_name='user_group_chat', on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Group Chats'
        ordering = ('created',)

    def __str__(self):
        return 'messages for {}'.format(self.business)


class ServiceCategories(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Service Categories'

    def __str__(self):
        return self.name


class Partners(models.Model):
    user = models.OneToOneField(User, related_name='user_partner', on_delete=models.CASCADE, null=True)
    service_category = models.ForeignKey(ServiceCategories, related_name='categories', on_delete=models.CASCADE, null=True)
    name_of_company = models.CharField(max_length=200, null=True)
    registration_number = models.IntegerField(null=True)
    location = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name_plural = 'Partners'

    def __str__(self):
        return self.user.username


class ServiceProviders(models.Model):
    user = models.OneToOneField(User, related_name='user_service', on_delete=models.CASCADE)
    service_category = models.ForeignKey(ServiceCategories, related_name='service_categ', on_delete=models.CASCADE,
                                         null=True)
    name_of_company = models.CharField(max_length=200, null=True)
    registration_number = models.IntegerField(null=True)
    location = models.CharField(max_length=200, null=True)
    country = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    service_description = models.TextField(null=True)


class PartnersPaymentNotes(models.Model):
    name = models.CharField(max_length=100, null=True)
    partner = models.ForeignKey(Partners, related_name='partners_pay', on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    notes = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Partners Payment Notes'

    def __str__(self):
        return self.partner.user.username


class CentinumServices(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Services(models.Model):
    service_name = models.ForeignKey(CentinumServices, related_name='centinum_services', on_delete=models.CASCADE, null=True)
    service_provider = models.ForeignKey(User, related_name='service_user', on_delete=models.CASCADE, null=True)
    client = models.ForeignKey(User, related_name='client_user', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    finished = models.BooleanField(default=False)
    service_cost = models.PositiveIntegerField(default=0)
    centinum_commission = models.PositiveIntegerField(default=0)
    sp_payment = models.PositiveIntegerField(default=0)

    def __str__(self):
        return 'services for {}'.format(self.client.username)

    def sp_payment(self):
        return self.service_cost - self.centinum_commission


class ServiceTimelineChats(models.Model):
    service = models.ForeignKey(Services, related_name='service_chats', on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    message = models.CharField(max_length=1000)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Chats for {}'.format(self.service)

    class Meta:
        verbose_name_plural = 'Service Timeline Chats'
        ordering = ('created',)


class Reports(models.Model):
    user = models.ForeignKey(User, related_name='user_reports', on_delete=models.CASCADE)
    reason = models.TextField()

    def __str__(self):
        return 'report made by {}'.format(self.user)


class ServiceProviderRatings(models.Model):
    rating = models.PositiveSmallIntegerField()
    review = models.TextField()
    s_provider = models.ForeignKey(User, related_name='sp_ratings', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'ratings for {}'.format(self.s_provider)









