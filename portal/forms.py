from django import forms
from .models import StartupBusiness, Ideas, IdeaInvestments, BusinessInvestments, GroupChats, Partners,\
    PartnersPaymentNotes, Services, ServiceProviders, ServiceTimelineChats, Reports, ServiceProviderRatings
from django_countries import Countries
from .models import BusinessImages
from djrichtextfield.widgets import RichTextWidget


class BusinessForm(forms.ModelForm):
    CHOICE1 = [
        ('Auction stage', 'Auction stage'),
        ('Idea stage', 'Idea stage'),
        ('Startup stage', 'Startup stage'),
        ('Growth stage', 'Growth stage'),
        ('Mature stage', 'Mature stage'),

    ]

    CHOICE3 = [
        ('Networking', 'Networking'),
        ('Partnership', 'Partnership'),
        ('Financing', 'Financing'),
        ('Mentorship', 'Mentorship')
    ]

    CHOICE2 = [
        ('B2B', 'B2B'),
        ('B2B2B', 'B2B2B'),
        ('B2B2C', 'B2B2C'),
        ('B2B2G', 'B2B2G'),
        ('B2C', 'B2C'),
        ('C2C', 'C2C'),
        ('Government(B2G)', 'Government(B2G)'),
        ('Non-profit', 'Non-Profit')
    ]
    country = forms.ChoiceField(label='Please select your country', widget=forms.Select, choices=Countries)
    founding_date = forms.DateField(widget=forms.DateInput(attrs={'placeholder': 'yyyy-mm-dd'}),
                                      label='Founding date')
    company_name = forms.CharField(widget=forms.TextInput, required=True)
    stage = forms.ChoiceField(choices=CHOICE1)
    sector = forms.ChoiceField(choices=CHOICE2)
    interest = forms.ChoiceField(choices=CHOICE3)

    class Meta:
        model = StartupBusiness
        fields = ('name', 'company_name','company_registration_number', 'customer_model', 'pitch', 'pitch_video_url', 'slogan','stake_you_are_giving_up', 'minimum_financing', 'financing_you_are_looking_for', 'sector', 'full_address', 'stage', 'country', 'founding_date', 'interest')


class BusinessForm2(forms.ModelForm):

    class Meta:
        model = StartupBusiness
        fields = ('financing_you_are_looking_for', 'minimum_financing', 'stake_you_are_giving_up')


class IdeaForm(forms.ModelForm):
    CHOICE3 = [
        ('Networking', 'Networking'),
        ('Partnership', 'Partnership'),
        ('Financing', 'Financing'),
        ('Mentorship', 'Mentorship')
    ]
    interest = forms.ChoiceField(choices=CHOICE3)

    class Meta:
        model = Ideas
        fields = ('name', 'description', 'interest', 'patent_number', 'copyright_number')


class BizInvestmentForm(forms.ModelForm):
    investor_amount = forms.DecimalField(label='Amount you are investing with')

    class Meta:
        model = BusinessInvestments
        fields = ('investor_amount',)


class BusinessImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')

    class Meta:
        model = BusinessImages
        fields = ('image', )


class GroupChatForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your message here...'}),
        label_suffix="")

    class Meta:
        model = GroupChats
        fields = ('message',)


class ServiceChat(forms.ModelForm):
    message = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type your message here...'}),
        label_suffix="")

    class Meta:
        model = ServiceTimelineChats
        fields = ('message',)


class PartnersForm(forms.ModelForm):
    country = forms.ChoiceField(label='Please select your country', widget=forms.Select, choices=Countries)

    class Meta:
        model = Partners
        fields = ('service_category', 'name_of_company', 'registration_number', 'country', 'city', 'location')


class ProvidersForm(forms.ModelForm):
    country = forms.ChoiceField(label='Please select your country', widget=forms.Select, choices=Countries)

    class Meta:
        model = ServiceProviders
        fields = ('service_category', 'name_of_company', 'registration_number', 'country', 'city', 'location',
                  'service_description')


class PartnersPaymentForm(forms.ModelForm):
    notes = forms.CharField(widget=RichTextWidget())

    class Meta:
        model = PartnersPaymentNotes
        fields = ('name', 'notes',)


class ServicesForm(forms.ModelForm):
    class Meta:
        model = Services
        fields = ()


class ReportForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = ('reason',)


class RatingsForm(forms.ModelForm):
    RATINGS = [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5)
    ]
    rating = forms.ChoiceField(choices=RATINGS)

    class Meta:
        model = ServiceProviderRatings
        fields = ('rating', 'review')







