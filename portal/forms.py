from django import forms
from .models import StartupBusiness, Ideas, IdeaInvestments, BusinessInvestments, GroupChats, Partners,\
    PartnersPaymentNotes, Services, ServiceProviders, ServiceTimelineChats, Reports, \
    ServiceProviderRatings, BusinessDirectInvestment, IdeaDirectInvestment, BusinessDirectInvestors,\
    IdeaDirectInvestors
from django_countries import Countries
from .models import BusinessImages
from djrichtextfield.widgets import RichTextWidget
from account.models import UserSubscriptions


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

    class Meta:
        model = StartupBusiness
        fields = ('name', 'company_name','company_registration_number', 'customer_model', 'pitch', 'pitch_video_url',
                  'slogan', 'sector', 'full_address', 'stage', 'country', 'founding_date', 'set_direct_investment')


class DirectInvestmentBizForm(forms.ModelForm):
    stake_you_are_giving_up = forms.CharField(widget=forms.NumberInput(attrs={'placeholder': 'this should be in (%) percentage'}))

    class Meta:
        model = BusinessDirectInvestment
        fields = ('business', 'financing_you_are_looking_for', 'minimum_financing', 'stake_you_are_giving_up',
                  'number_of_investors')

    def __init__(self, request, *args, **kwargs):
        super(DirectInvestmentBizForm, self).__init__(*args, **kwargs)
        try:
            self.fields['business'].queryset = StartupBusiness.objects.filter(set_direct_investment=True, user=request.user)
        except StartupBusiness.DoesNotExist:
            ### there is not userextend corresponding to this user, do what you want
            raise Exception('object does not exist')
            pass


class DirectInvestmentIdeaForm(forms.ModelForm):
    stake_you_are_giving_up = forms.CharField(
        widget=forms.NumberInput(attrs={'placeholder': 'this should be in (%) percentage'}))

    class Meta:
        model = IdeaDirectInvestment
        fields = ('idea', 'financing_you_are_looking_for', 'minimum_financing', 'stake_you_are_giving_up',
                  'number_of_investors')

    def __init__(self, request, *args, **kwargs):
        super(DirectInvestmentIdeaForm, self).__init__(*args, **kwargs)
        try:
            self.fields['idea'].queryset = Ideas.objects.filter(set_direct_investment=True, user=request.user)
        except Ideas.DoesNotExist:
            ### there is not userextend corresponding to this user, do what you want
            raise Exception('object does not exist')
            pass

# class BusinessForm2(forms.ModelForm):
#
#     class Meta:
#         model = StartupBusiness
#         fields = ('financing_you_are_looking_for', 'minimum_financing', 'stake_you_are_giving_up')


class IdeaForm(forms.ModelForm):

    class Meta:
        model = Ideas
        fields = ('name', 'description', 'patent_number', 'copyright_number', 'set_direct_investment')



# class BizInvestmentForm(forms.ModelForm):
#     investor_amount = forms.DecimalField(label='Amount you are investing with')
#
#     class Meta:
#         model = BusinessInvestments
#         fields = ('investor_amount',)


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
        fields = ('name', 'amount', 'notes',)


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


class IdeaDirectInvestorsForm(forms.ModelForm):

    class Meta:
        model = IdeaDirectInvestors
        fields = ('amount_investing', )


class BizDirectInvestorsForm(forms.ModelForm):

    class Meta:
        model = BusinessDirectInvestors
        fields = ('amount_investing', )










