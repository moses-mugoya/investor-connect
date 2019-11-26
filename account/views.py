from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserEditForm, ChatForm, SearchForm, VerificationForm
from .forms import ProfileEditForm, BusinessManagementForm
from .models import Profile, Chat, User, Plans, UserSubscriptions
from portal.models import Ideas, StartupBusiness, BusinessInvestments, IdeaInvestments, CentinumVentures,\
    BusinessImages, Partners, PartnersPaymentNotes, Services, ServiceProviders, BusinessDirectInvestment,\
    IdeaDirectInvestment, IdeaDirectInvestors, BusinessDirectInvestors
from portal.forms import IdeaForm, BusinessForm, BusinessImageForm, PartnersForm, PartnersPaymentForm, \
    ProvidersForm, ReportForm, DirectInvestmentBizForm, DirectInvestmentIdeaForm
from django.contrib.postgres.search import SearchVector
from django.forms import modelformset_factory
from django.core.mail import send_mail
from django.conf import settings


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)

        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            if user_form.cleaned_data['usertype'] == 'Innovator':
                new_user.is_innovator = True
            elif user_form.cleaned_data['usertype'] == 'Entrepreneur':
                new_user.is_entrepreneur = True
            elif user_form.cleaned_data['usertype'] == 'Investor':
                new_user.is_investor = True
            elif user_form.cleaned_data['usertype'] == 'Partner':
                new_user.is_partner = True
            elif user_form.cleaned_data['usertype'] == 'Service Provider':
                new_user.is_service_provider = True
            # Save the User object
            new_user.save()
            # Create the user profile
            if new_user.is_partner:
                Partners.objects.create(user=new_user)
            if new_user.is_service_provider:
                ServiceProviders.objects.create(user=new_user)
            profile = Profile.objects.create(user=new_user)

            return render(request,
                          'account/register_done.html',
                          {'new_user': new_user})
        else:
            messages.error(request, 'We encountered an error,please check your details and try again')
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profiles,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('account:profile')
            # messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profiles)
    return render(request, 'account/edit.html', {'user_form': user_form,
                                                 'profile_form': profile_form})


def profile(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    partner_user = None
    user_form = None
    profile_form = None
    idea_form2 = None
    business_form = None
    pat_edit_form = None
    provider_form = None
    report_form = None
    partner_notes_form = None
    biz_direct_form = None
    idea_direct_form = None
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    current_user_subscription = str(current_user_subscription.plan_category)
    idea_direct_invest = IdeaDirectInvestment.objects.filter(user=request.user)
    biz_direct_invest = BusinessDirectInvestment.objects.filter(user=request.user)
    if request.user.is_partner:
        partner_user = request.user.user_partner
    services = Services.objects.filter(client=request.user)
    provider_services = Services.objects.filter(service_provider=request.user)
    biz_investment_requests = BusinessInvestments.objects.filter(business__user=request.user)
    print(biz_investment_requests)
    idea_investment_requests = IdeaInvestments.objects.filter(idea__user=request.user)
    profile = get_object_or_404(Profile, user=request.user)
    centinum = CentinumVentures.objects.all()
    centinum_count = centinum.count()
    ideas = Ideas.objects.filter(user=request.user, set_direct_investment=False)
    ideas_count = ideas.count()
    startup = StartupBusiness.objects.filter(set_direct_investment=False)
    user_biz = StartupBusiness.objects.filter(user=request.user, set_direct_investment=False)
    user_biz_direct = StartupBusiness.objects.filter(user=request.user, set_direct_investment=True)
    user_biz_count = user_biz.count()
    user_idea = Ideas.objects.filter(user=request.user, set_direct_investment=False)
    user_idea_count = user_idea.count()
    startup_count = startup.count()
    biz_investments = BusinessInvestments.objects.filter(investor=request.user)
    biz_investment_count = biz_investments.count()
    investments = IdeaInvestments.objects.filter(investor=request.user)
    investment_count = investments.count()
    partners = Partners.objects.all()
    payment_notes = PartnersPaymentNotes.objects.filter(partner=partner_user)
    patner = []
    for pat in partners:
        patner.append(pat.user)
    providers_list = ServiceProviders.objects.all()
    provider = []

    for pro in providers_list:
        provider.append(pro.user)

    if request.method == 'POST':
        if 'profile_data' in request.POST:
            user_form = UserEditForm(instance=request.user,
                                     data=request.POST)
            profile_form = ProfileEditForm(instance=request.user.profiles,
                                           data=request.POST,
                                           files=request.FILES)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect('account:profile')
            else:
                messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profiles)

    # adding a new idea
    if request.method == 'POST':
        if 'idea_add' in request.POST:
            idea_form2 = IdeaForm(data=request.POST)
            if idea_form2.is_valid():
                current_user_subscription = UserSubscriptions.objects.get(user=request.user)
                current_user_subscription = current_user_subscription.plan
                all_ideas = Ideas.objects.filter(user=request.user)
                all_ideas_count = all_ideas.count()
                print(current_user_subscription.plan_category)
                if str(current_user_subscription.plan_category) == 'Free':
                    if all_ideas_count >= 1:
                        messages.error(request, "You have already added {} idea(s) Please upgrade your membership to be able to add more ideas".format(all_ideas_count))
                    else:
                        new_idea_form = idea_form2.save(commit=False)
                        new_idea_form.user = request.user
                        new_idea_form.save()
                        messages.success(request, 'Idea added successfully')
                        return redirect('account:profile')
                elif str(current_user_subscription.plan_category) == 'Startup':
                    if all_ideas_count >= 1:
                        messages.error(request, "You have already added {} idea(s) Please upgrade your membership to be able to add more ideas".format(all_ideas_count))
                    else:
                        new_idea_form = idea_form2.save(commit=False)
                        new_idea_form.user = request.user
                        new_idea_form.save()
                        messages.success(request, 'Idea added successfully')
                        return redirect('account:profile')
                elif str(current_user_subscription.plan_category) == 'Pro':
                    if all_ideas_count >= 3:
                        messages.error(request, "You have already added {} idea(s) Please upgrade your membership to be able to add more ideas".format(all_ideas_count))
                    else:
                        new_idea_form = idea_form2.save(commit=False)
                        new_idea_form.user = request.user
                        new_idea_form.save()
                        messages.success(request, 'Idea added successfully')
                        return redirect('account:profile')
                elif str(current_user_subscription.plan_category) == 'Enterprise':
                    if all_ideas_count >= 5:
                        messages.error(request, "You have already added {} idea(s) Please upgrade your membership to be able to add more ideas".format(all_ideas_count))
                    else:
                        new_idea_form = idea_form2.save(commit=False)
                        new_idea_form.user = request.user
                        new_idea_form.save()
                        messages.success(request, 'Idea added successfully')
                        return redirect('account:profile')

            else:
                messages.error(request, 'Error adding your idea! Please check your details ')
    else:
        idea_form2 = IdeaForm()

    # add business form
    if request.method == 'POST':
        if 'business_add' in request.POST:
            business_form = BusinessForm(data=request.POST)
            if business_form.is_valid():
                current_user_subscription = UserSubscriptions.objects.get(user=request.user)
                current_user_subscription = current_user_subscription.plan
                all_biz = StartupBusiness.objects.filter(user=request.user)
                all_biz_count = all_biz.count()
                print(current_user_subscription.plan_category)
                if str(current_user_subscription.plan_category) == 'Free':
                    print("this is being free")
                    if all_biz_count >= 1:
                        messages.error(request,
                                       "You have already added {} startup(s) Please upgrade your membership to be able to add more startup".format(
                                           all_biz_count))
                    else:
                        new_business_form = business_form.save(commit=False)
                        new_business_form.user = request.user
                        new_business_form.save()
                        messages.success(request, "Start up added successfully")

                        return redirect('account:profile')
                elif str(current_user_subscription.plan_category) == 'Startup':
                    print("this is being startup")
                    if all_biz_count >= 1:
                        messages.error(request,
                                       "You have already added {} startup(s) Please upgrade your membership to be able to add more startups".format(
                                           all_biz_count))
                    else:
                        new_business_form = business_form.save(commit=False)
                        new_business_form.user = request.user
                        new_business_form.save()
                        messages.success(request, "Start up added successfully")

                        return redirect('account:profile')
                elif str(current_user_subscription.plan_category) == 'Pro':
                    print("this is being pro")
                    if all_biz_count >= 3:
                        messages.error(request,
                                       "You have already added {} Startup(s) Please upgrade your membership to be able to add more startups".format(
                                           all_biz_count))
                    else:
                        new_business_form = business_form.save(commit=False)
                        new_business_form.user = request.user
                        new_business_form.save()
                        messages.success(request, "Start up added successfully")
                        return redirect('account:profile')
                elif str(current_user_subscription.plan_category) == 'Enterprise':
                    print("this is being entreprsie")
                    if all_biz_count >= 5:
                        messages.error(request,
                                       "You have already added {} Startup(s) Please upgrade your membership to be able to add more ideas".format(
                                           all_biz_count))
                    else:
                        new_business_form = business_form.save(commit=False)
                        new_business_form.user = request.user
                        new_business_form.save()
                        messages.success(request, "Start up added successfully")
                        return redirect('account:profile')
            else:
                messages.error(request, "Error adding startup")
    else:
        business_form = BusinessForm()

    # add a direct business investment
    if request.method == 'POST':
        if 'biz_direct_button' in request.POST:
            biz_direct_form = DirectInvestmentBizForm(data=request.POST, request=request)
            if biz_direct_form.is_valid():
                new_biz = biz_direct_form.save(commit=False)
                new_biz.user = request.user
                new_biz.save()
                messages.success(request, "Start up updated successfully for direct investment")
            else:
                messages.error(request, "Error updating startup for direct investment")
    else:
        biz_direct_form = DirectInvestmentBizForm(request=request)

    # add a direct idea investment
    if request.method == 'POST':
        if 'idea_direct_button' in request.POST:
            idea_direct_form = DirectInvestmentIdeaForm(data=request.POST, request=request)
            if idea_direct_form.is_valid():
                new_biz = idea_direct_form.save(commit=False)
                new_biz.user = request.user
                new_biz.save()
                messages.success(request, "Idea updated successfully for direct investment")
            else:
                messages.error(request, "Error updating idea for direct investment")
    else:
        idea_direct_form = DirectInvestmentIdeaForm(request=request)

    # report form
    if request.method == 'POST':
        if 'report' in request.POST:
            report_form = ReportForm(data=request.POST)
            if report_form.is_valid():
                new_form = report_form.save(commit=False)
                new_form.user = request.user
                new_form.save()
                messages.success(request, 'Report received successfully')
                return redirect('account:profile')
            else:
                messages.error(request, 'Error sending your report')
    else:
        report_form = ReportForm()

        # edit partner details
    myuser = None
    if request.user.is_partner:
        myuser = request.user.user_partner
    if request.method == 'POST':
        if 'partner_edit' in request.POST:
                pat_edit_form = PartnersForm(data=request.POST, instance=myuser)
                if pat_edit_form.is_valid():
                    pat_edit_form.save()
                    messages.success(request, "Updated successfully")
                    return redirect('account:profile')
                else:
                    messages.error(request, "Error updating")
    else:
        pat_edit_form = PartnersForm(instance=myuser)

    # # add partner details
    # if request.method == 'POST':
    #     pat_form = PartnersForm(data=request.POST)
    #     if pat_form.is_valid():
    #         new_pat_form = pat_form.save(commit=False)
    #         new_pat_form.user = request.user
    #         new_pat_form.save()
    #         return redirect('account:profile')
    # else:
    #     pat_form = PartnersForm()

    # edit service provider details
    prov_user = None
    if request.user.is_service_provider:
        prov_user = request.user.user_service
    if request.method == 'POST':
        if 'provider_edit' in request.POST:
            provider_form = ProvidersForm(data=request.POST, instance=prov_user)
            if provider_form.is_valid():
                provider_form.save()
                messages.success(request, "Details updated successfully")
                return redirect('account:profile')
            else:
                messages.error(request, "Error updating your details")
    else:
        provider_form = ProvidersForm(instance=prov_user)

    # add service provider details
    # if request.method == 'POST':
    #     pro_add_form = ProvidersForm(data=request.POST)
    #     if pro_add_form.is_valid():
    #         new_form = pro_add_form.save(commit=False)
    #         new_form.user = request.user
    #         new_form.save()
    #         return redirect('account:profile')
    # else:
    #     pro_add_form = ProvidersForm()

    # Partner payment form
    if request.method == 'POST':
        if 'partner_notes_button' in request.POST:
            partner_notes_form = PartnersPaymentForm(data=request.POST)
            if partner_notes_form.is_valid():
                new_form = partner_notes_form.save(commit=False)
                new_form.partner = partner_user
                new_form.save()
                messages.success(request, "Note added successfully")
                return redirect('account:profile')
            else:
                messages.error(request, "Error adding the note")
    else:
        partner_notes_form = PartnersPaymentForm()

    return render(request, 'account/profile.html', {'profile': profile,
                                                    'biz_investment_requests': biz_investment_requests,
                                                    'idea_investment_requests': idea_investment_requests,
                                                    'centinum': centinum,
                                                    'centinum_count': centinum_count,
                                                    'startup_count': startup_count,
                                                    'ideas_count': ideas_count,
                                                    'biz_investments': biz_investments,
                                                    'biz_investment_count': biz_investment_count,
                                                    'investments': investments,
                                                    'investment_count': investment_count,
                                                    'user_form': user_form,
                                                    'profile_form': profile_form,
                                                    'user_biz': user_biz,
                                                    'user_biz_count': user_biz_count,
                                                    'user_idea': user_idea,
                                                    'user_idea_count': user_idea_count,
                                                    'idea_form2': idea_form2,
                                                    'business_form': business_form,
                                                    'patner': patner,
                                                    'pat_edit_form': pat_edit_form,
                                                    'partner_notes_form': partner_notes_form,
                                                    'payment_notes': payment_notes,
                                                    'services': services,
                                                    'provider_form': provider_form,
                                                    'provider': provider,
                                                    'provider_services': provider_services,
                                                    'report_form': report_form,
                                                    'key': key,
                                                    'user_biz_direct': user_biz_direct,
                                                    'biz_direct_form': biz_direct_form,
                                                    'idea_direct_form': idea_direct_form,
                                                    'idea_direct_invest': idea_direct_invest,
                                                    'biz_direct_invest': biz_direct_invest,
                                                    'current_user_subscription': current_user_subscription,
                                                    })


def edit_partner_note(request, id):
    partner_notes_form = None
    note = PartnersPaymentNotes.objects.get(id=id)
    if request.method == 'POST':
        if 'partner_notes_button' in request.POST:
            partner_notes_form = PartnersPaymentForm(data=request.POST, instance=note)
            if partner_notes_form.is_valid():
                new_form = partner_notes_form.save(commit=False)
                new_form.save()
                messages.success(request, "Note updated successfully")
                return redirect('account:profile')
            else:
                messages.error(request, "Error updating the note")
    else:
        partner_notes_form = PartnersPaymentForm(instance=note)
    return render(request, 'account/edit_note.html', {'partner_notes_form': partner_notes_form})


def profiles_list(request):
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    current_user_subscription = str(current_user_subscription.plan_category)
    user_profiles = Profile.objects.filter(user__is_verified=True).exclude(user=request.user)
    print(user_profiles)
    return render(request, 'account/profile_list.html', {'user_profiles': user_profiles,
                                                         'current_user_subscription': current_user_subscription})


def profile_list_investors(request):
    user_profiles = Profile.objects.filter(user__is_verified=True, user__is_investor=True).exclude(user=request.user)
    return render(request, 'account/investors.html', {'user_profiles': user_profiles})


def profile_list_enterps(request):
    user_profiles = Profile.objects.filter(user__is_verified=True, user__is_entrepreneur=True).exclude(user=request.user)
    return render(request, 'account/entreps.html', {'user_profiles': user_profiles})


def profile_list_innovators(request):
    user_profiles = Profile.objects.filter(user__is_verified=True, user__is_innovator=True).exclude(user=request.user)
    return render(request, 'account/innovators.html', {'user_profiles': user_profiles})


def profile_detail(request, id):
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    current_user_subscription = str(current_user_subscription.plan_category)
    dir_idea_investors = IdeaDirectInvestors.objects.all()
    dir_idea_investors_array = []
    for dir in dir_idea_investors:
        dir_idea_investors_array.append(dir.investor)
    current_user = get_object_or_404(Profile, user=request.user)
    user_profile = get_object_or_404(Profile, id=id)
    startups = StartupBusiness.objects.filter(user=user_profile.user, set_direct_investment=False)
    ideas = Ideas.objects.filter(user=user_profile.user, set_direct_investment=False)
    biz_direct_investments = BusinessDirectInvestment.objects.filter(user=user_profile.user, approved=True)
    idea_direct_investments = IdeaDirectInvestment.objects.filter(user=user_profile.user, approved=True)
    return render(request, 'account/profile_detail.html', {'user_profile': user_profile,
                                                           'startups': startups,
                                                           'ideas': ideas,
                                                           'current_user': current_user,
                                                           'biz_direct_investments': biz_direct_investments,
                                                           'idea_direct_investments': idea_direct_investments,
                                                           'dir_idea_investors_array': dir_idea_investors_array,
                                                           'current_user_subscription': current_user_subscription})


def chat_view(request, receiver):
    chats = Chat.objects.filter(sender=request.user, receiver__username=receiver) | Chat.objects.filter(sender__username=receiver, receiver__username=request.user)
    receiver_user = get_object_or_404(Profile, user__username=receiver)
    if request.method == 'POST':
        chat_form = ChatForm(data=request.POST)
        if chat_form.is_valid():
            user_text = chat_form.cleaned_data['message']
            user_text = user_text.lower()
            if 'money' in user_text or 'cash' in user_text or 'payment' in user_text:
                messages.error(request, 'Your text contains unwanted phrases')
            else:
                new_form = chat_form.save(commit=False)
                new_form.sender = request.user
                new_form.receiver = receiver_user.user
                new_form.save()
                chat_form = ChatForm()
    else:
        chat_form = ChatForm()
    return render(request, 'account/chats.html', {'chats': chats, 'chat_form': chat_form, 'receiver_user': receiver_user})


def user_search(request):
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    current_user_subscription = str(current_user_subscription.plan_category)
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = User.objects.annotate(
                search=SearchVector('username'),
            ).filter(search=query)
    return render(request,
                  'account/search.html',
                  {'form': form,
                   'query': query,
                   'results': results,
                   'current_user_subscription': current_user_subscription})


@login_required
def verify_user(request):
    if request.method == 'POST':
        ver_form = VerificationForm(data=request.POST, files=request.FILES)
        if ver_form.is_valid():
            new_verform = ver_form.save(commit=False)
            new_verform.user = request.user
            new_verform.save()
            sender = 'centinum@gmail.com'
            subject = 'Profile Pending Approval'
            message = 'Hi {}, we have received your application to join Centinum. ' \
                      'We will review your profile and get back to you'.format(request.user.username)
            receiver = request.user.email
            send_mail(subject, message, sender, [receiver])
            return redirect('account:verification_done')
    else:
        ver_form = VerificationForm()
    return render(request, 'account/verification.html', {'ver_form': ver_form})


def verification_done(request):
    return render(request, 'account/verification_done.html')


def business_management(request):
    if request.method == 'POST':
        management_form = BusinessManagementForm(data=request.POST)
        if management_form.is_valid():
            management_form.save()
            messages.success(request, "Message sent successfully")
        else:
            messages.error(request, "Error sending the message")
    else:
        management_form = BusinessManagementForm()
    return render(request, 'account/contact.html', {'management_form': management_form})


