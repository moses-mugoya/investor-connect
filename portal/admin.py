from django.contrib import admin
from .models import StartupBusiness, Ideas, \
    BusinessInvestments, IdeaInvestments, IdeaTeams, BusinessTeams,\
    CentinumVentures, BusinessImages, GroupChats, Partners, ServiceCategories, PartnersPaymentNotes, Services, \
    CentinumServices, ServiceProviders, Reports, ServiceProviderRatings

from account.models import User


class StartAppAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'created', 'financing_you_are_looking_for', 'stake_you_are_giving_up', 'minimum_financing', 'modified', 'interest', 'company_name', 'customer_model', 'pitch_video_url']
    list_filter = ['user', 'created']


admin.site.register(StartupBusiness, StartAppAdmin)


class IdeasAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'interest', 'created', 'modified']
    list_filter = ['user', 'created']


admin.site.register(Ideas, IdeasAdmin)


class AdminIdeaInvestments(admin.ModelAdmin):
    list_display = ['idea', 'investor', 'created', 'modified', 'approved']
    list_editable = ['approved']
    list_filter = ['idea', 'approved', 'investor']


admin.site.register(IdeaInvestments, AdminIdeaInvestments)


class AdminBusinessInvestments(admin.ModelAdmin):
    list_display = ['business', 'investor', 'investor_amount', 'created', 'modified', 'approved']
    list_editable = ['approved']
    list_filter = ['business', 'approved', 'investor']


admin.site.register(BusinessInvestments, AdminBusinessInvestments)


class AdminBusinessTeams(admin.ModelAdmin):
    list_display = ['business', 'member', 'created', 'modified']
    list_filter = ['business',  'member']


admin.site.register(BusinessTeams, AdminBusinessTeams)


class AdminIdeaTeams(admin.ModelAdmin):
    list_display = ['idea', 'member', 'created', 'modified']
    list_filter = ['idea',  'member']


admin.site.register(IdeaTeams, AdminIdeaTeams)


class CentinumAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'amount', 'percentage', 'minimum_amount', 'modified', 'interest',
                    'company_name', 'customer_model', 'pitch_video_url']
    list_filter = ['created']


admin.site.register(CentinumVentures, CentinumAdmin)


class BusinessImagesAdmin(admin.ModelAdmin):
    list_display = ['business']


admin.site.register(BusinessImages, BusinessImagesAdmin)


class GroupChatAdmin(admin.ModelAdmin):
    list_display = ['user', 'business', 'message', 'created', 'modified']
    list_filter = ['business']


admin.site.register(GroupChats, GroupChatAdmin)


class PartnerAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_category', 'name_of_company', 'registration_number', 'location', 'country', 'city']
    list_filter = ['service_category']


admin.site.register(Partners, PartnerAdmin)


class ProviderAdmin(admin.ModelAdmin):
    list_display = ['user', 'service_category', 'name_of_company', 'registration_number', 'location', 'country', 'city']
    list_filter = ['service_category']


admin.site.register(ServiceProviders, ProviderAdmin)


class ServiceCatAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'modified']
    list_filter = ['name']


admin.site.register(ServiceCategories, ServiceCatAdmin)


class PartnersPaymentAdmin(admin.ModelAdmin):
    list_display = ['name', 'partner', 'created', 'modified', 'paid']
    list_filter = ['paid']


admin.site.register(PartnersPaymentNotes, PartnersPaymentAdmin)


class CentinumServicesAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'modified']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(CentinumServices, CentinumServicesAdmin)


class ServicesAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "service_provider":
            kwargs["queryset"] = User.objects.filter(is_service_provider=True)
        return super(ServicesAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ['service_name', 'service_provider', 'client', 'created', 'modified', 'finished', 'accepted',
                    'service_cost', 'centinum_commission', 'sp_payment']
    list_editable = ['accepted']


admin.site.register(Services, ServicesAdmin)


class ReportAdmin(admin.ModelAdmin):
    list_display = ['user', 'reason']
    list_display_links = ['user']
    list_filter = ['user']


admin.site.register(Reports, ReportAdmin)


class RatingAdmin(admin.ModelAdmin):
    list_display = ['s_provider', 'rating', 'created']


admin.site.register(ServiceProviderRatings, RatingAdmin)




