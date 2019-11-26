import stripe
from django.views.generic.base import TemplateView
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BusinessForm, IdeaForm, \
    BusinessImageForm, GroupChatForm, PartnersForm, PartnersPaymentForm, ServicesForm, ServiceChat, \
    RatingsForm, DirectInvestmentBizForm, BizDirectInvestorsForm, IdeaDirectInvestorsForm
from .models import Ideas, StartupBusiness, IdeaInvestments, BusinessInvestments, \
    BusinessTeams, IdeaTeams, CentinumVentures, BusinessImages, Partners, CentinumServices, Services,\
    PartnersPaymentNotes, BusinessDirectInvestment, IdeaDirectInvestment, BusinessDirectInvestors, IdeaDirectInvestors
from django.contrib.auth.decorators import login_required
from account.models import Profile, User, UserSubscriptions, Plans, PlanCategories, Subscriptions
from .decorators import innovator_required, investor_required, entrepreneur_required, verification_required
from django.contrib import messages
from django.urls import reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.forms import modelformset_factory
from account.forms import SearchForm
from django.contrib.postgres.search import SearchVector
from datetime import datetime

stripe.api_key = settings.STRIPE_SECRET_KEY


def index(request):
    return render(request, 'portal/index.html')


@login_required(login_url='/centinum/login/')
@require_POST
def business_like(request):
    business_id = request.POST.get('id')
    action = request.POST.get('action')
    if business_id and action:
        try:
            business = StartupBusiness.objects.get(id=business_id)
            if action == 'like':
                business.users_like.add(request.user)
                sender = 'centinum@gmail.com'
                subject = 'Profile Liked'
                message = 'Hi {}, someone liked your profile on Centinum'.format(business.user)
                send_mail(subject, message, sender, [business.user.email])

            else:
                business.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required(login_url='/centinum/login/')
@require_POST
def idea_like(request):
    print("This will be executed")
    idea_id = request.POST.get('id')
    action = request.POST.get('action')
    if idea_id and action:
        try:
            idea = Ideas.objects.get(id=idea_id)
            if action == 'like':

                idea.users_like.add(request.user)
                sender = 'centinum@gmail.com'
                subject = 'Profile Liked'
                message = 'Hi {}, someone liked your profile on Centinum'.format(idea.user)
                send_mail(subject, message, sender, [idea.user.email])

            else:
                idea.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ko'})


@login_required(login_url='loginApp:login')
@verification_required
def home(request):
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    current_user_subscription = str(current_user_subscription.plan_category)
    print(current_user_subscription)
    ideas = Ideas.objects.filter(user=request.user, set_direct_investment=False)
    ideas_count = ideas.count()
    startup = StartupBusiness.objects.filter(set_direct_investment=False)
    startup_count = startup.count()
    centinum = CentinumVentures.objects.all()
    centinum_count = centinum.count()
    return render(request, 'portal/home.html',
                  {'centinum': centinum,
                   'centinum_count': centinum_count,
                   'ideas': ideas,
                   'ideas_count': ideas_count,
                   'startup': startup,
                   'startup_count': startup_count,
                   'current_user_subscription': current_user_subscription})


@login_required
def centinum(request):
    ideas = Ideas.objects.all()
    ideas_count = ideas.count()
    startup = StartupBusiness.objects.filter(set_direct_investment=False)
    startup_count = startup.count()
    centinum = CentinumVentures.objects.all()
    centinum_count = centinum.count()
    services = CentinumServices.objects.all()
    return render(request, 'portal/centinum.html',
                  {'centinum': centinum, 'centinum_count': centinum_count, 'ideas': ideas,
                   'ideas_count': ideas_count,
                   'startup': startup,
                   'startup_count': startup_count,
                   'services': services})


@login_required
def home_biz(request):
    ideas = Ideas.objects.all()
    ideas_count = ideas.count()
    startup = StartupBusiness.objects.filter(set_direct_investment=False)
    startup_count = startup.count()
    centinum = CentinumVentures.objects.all()
    centinum_count = centinum.count()
    return render(request, 'portal/home_biz.html',
                  {'centinum': centinum, 'centinum_count': centinum_count, 'ideas': ideas, 'ideas_count': ideas_count,
                   'startup': startup, 'startup_count': startup_count})


@investor_required
@login_required
def investor(request):
    startup = StartupBusiness.objects.all()
    startup_count = StartupBusiness.objects.count()
    return render(request, 'portal/investor.html', {'startup': startup, 'startup_count': startup_count})


@investor_required
@login_required
def investor_idea(request):
    ideas = Ideas.objects.all()
    ideas_count = Ideas.objects.count()
    return render(request, 'portal/investor_idea.html', {'ideas': ideas, 'ideas_count': ideas_count})


@innovator_required
@login_required
def innovator(request):
    ideas = Ideas.objects.filter(user=request.user)
    ideas_count = Ideas.objects.filter(user=request.user).count()
    return render(request, 'portal/innovator.html', {'ideas': ideas, 'ideas_count': ideas_count})


@entrepreneur_required
@login_required
def entrepreneur(request):
    startup = StartupBusiness.objects.filter(user=request.user)
    startup_count = StartupBusiness.objects.count()
    return render(request, 'portal/entrepreneur.html', {'startup': startup, 'startup_count': startup_count})


def business_detail(request, id):
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    current_user_subscription = str(current_user_subscription.plan_category)
    biz_direct = BusinessDirectInvestment.objects.all()
    biz_direct_count = biz_direct.count()
    team_members = []
    all_investors = []
    business = get_object_or_404(StartupBusiness, id=id)
    dir_biz_investors = business.direct_biz_invest.all()
    dir_biz_investors_array = []
    for dir in dir_biz_investors:
        dir_biz_investors_array.append(dir.investor)
    images = BusinessImages.objects.filter(business=business)
    team_biz = business.team_business.all()
    for team_mem in team_biz:
        team_members.append(team_mem.member)

    centinum = CentinumVentures.objects.all()
    centinum_count = centinum.count()
    ideas = Ideas.objects.all()
    ideas_count = ideas.count()
    startup = StartupBusiness.objects.all()
    startup_count = startup.count()
    profile = get_object_or_404(Profile, user=request.user)
    # min_amount_per = (business.minimum_financing * business.stake_you_are_giving_up) / business.financing_you_are_looking_for
    # min_amount_per = round(min_amount_per, 2)
    # invest_per = 0
    investors = business.invest_business.filter(approved=True)
    for inv in investors:
        all_investors.append(inv.investor)
    investors_count = business.invest_business.filter(approved=True).count()
    # if request.method == 'POST':
    #     biz_invest_form = BizInvestmentForm(data=request.POST)
    #     if biz_invest_form.is_valid():
    #         invest_amount = biz_invest_form.cleaned_data['investor_amount']
    #         if invest_amount < business.minimum_financing:
    #             messages.error(request, "The minimum amount required is {}".format(business.minimum_financing))
    #             return redirect('portal:business_detail', business.id)
    #         invest_per = (invest_amount * business.stake_you_are_giving_up) / business.financing_you_are_looking_for
    #         invest_per = round(invest_per, 2)
    #         new_form = biz_invest_form.save(commit=False)
    #         new_form.investor = request.user
    #         new_form.business = business
    #         new_form.save()
    #         messages.success(request,
    #                          "Investment successful! You have invested KSH {} which is {}%".format(invest_amount,
    #                                                                                                invest_per))
    #         return redirect('portal:business_detail', business.id)
    #
    # else:
    #     biz_invest_form = BizInvestmentForm()

    if request.method == 'POST':
        business_form = BusinessForm(data=request.POST, instance=business)
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.save()
            return redirect('account:profile')
    else:
        business_form = BusinessForm(instance=business)

    return render(request, 'portal/business_detail.html', {'business': business,
                                                           'images': images,
                                                           'centinum': centinum,
                                                           'centinum_count': centinum_count,
                                                           'profile': profile,
                                                           'ideas': ideas,
                                                           'ideas_count': ideas_count,
                                                           'startup': startup,
                                                           'startup_count': startup_count,
                                                           'investors': investors,
                                                           'investors_count': investors_count,
                                                           'business_form': business_form,
                                                           'team_members': team_members,
                                                           'all_investors': all_investors,
                                                           'team_biz': team_biz,
                                                           'biz_direct_count': biz_direct_count,
                                                           'dir_biz_investors_array': dir_biz_investors_array,
                                                           'dir_biz_investors': dir_biz_investors,
                                                           'current_user_subscription': current_user_subscription
                                                           })


def direct_biz_invest(request, id):
    biz_direct = BusinessDirectInvestors.objects.all()
    biz_direct_count = biz_direct.count()
    direct_biz = BusinessDirectInvestment.objects.get(id=id)
    print(biz_direct_count)
    business = direct_biz.business
    min_amount_per = (direct_biz.minimum_financing * direct_biz.stake_you_are_giving_up) / direct_biz.financing_you_are_looking_for
    min_amount_per = round(min_amount_per, 2)
    invest_per = 0
    if request.method == 'POST':
        biz_invest_form = BizDirectInvestorsForm(data=request.POST)
        if biz_invest_form.is_valid():
            invest_amount = biz_invest_form.cleaned_data['amount_investing']
            if invest_amount < direct_biz.minimum_financing:
                messages.error(request, "The minimum amount required is {}".format(direct_biz.minimum_financing))
            elif invest_amount > direct_biz.financing_you_are_looking_for:
                messages.error(request, "You have invested more than is required. Reduce the amount and try again")
            elif biz_direct_count == direct_biz.number_of_investors:
                messages.error(request, "There is already enough investors required")
            else:
                invest_per = (invest_amount * direct_biz.stake_you_are_giving_up) / direct_biz.financing_you_are_looking_for
                invest_per = round(invest_per, 2)
                new_form = biz_invest_form.save(commit=False)
                new_form.investor = request.user
                new_form.business = business
                new_form.percentage_stake = invest_per
                new_form.save()
                messages.success(request,
                                 "Investment successful! You have invested KSH {} which is {}%".format(invest_amount,
                                                                                                       invest_per))
                return redirect('account:profile')

    else:
        biz_invest_form = BizDirectInvestorsForm()
    return render(request, 'portal/biz_direct_investors.html', {'biz_invest_form': biz_invest_form, })


def direct_idea_invest(request, id):
    dir_idea_investors = IdeaDirectInvestors.objects.all()
    dir_idea_investors_array = []
    for dir in dir_idea_investors:
        dir_idea_investors_array.append(dir.investor)
    biz_direct = IdeaDirectInvestors.objects.all()
    biz_direct_count = biz_direct.count()
    direct_biz = IdeaDirectInvestment.objects.get(id=id)
    idea = direct_biz.idea
    print(biz_direct_count)
    min_amount_per = (direct_biz.minimum_financing * direct_biz.stake_you_are_giving_up) / direct_biz.financing_you_are_looking_for
    min_amount_per = round(min_amount_per, 2)
    invest_per = 0
    if request.method == 'POST':
        biz_invest_form = IdeaDirectInvestorsForm(data=request.POST)
        if biz_invest_form.is_valid():
            invest_amount = biz_invest_form.cleaned_data['amount_investing']
            if invest_amount < direct_biz.minimum_financing:
                messages.error(request, "The minimum amount required is {}".format(direct_biz.minimum_financing))
            elif invest_amount > direct_biz.financing_you_are_looking_for:
                messages.error(request, "You have invested more than is required. Reduce the amount and try again")
            elif biz_direct_count == direct_biz.number_of_investors:
                messages.error(request, "There is already enough investors required")
            else:
                invest_per = (invest_amount * direct_biz.stake_you_are_giving_up) / direct_biz.financing_you_are_looking_for
                invest_per = round(invest_per, 2)
                new_form = biz_invest_form.save(commit=False)
                new_form.investor = request.user
                new_form.idea = idea
                new_form.percentage_stake = invest_per
                new_form.save()
                messages.success(request,
                                 "Investment successful! You have invested KSH {} which is {}%".format(invest_amount,
                                                                                                       invest_per))
                return redirect('account:profile')

    else:
        biz_invest_form = IdeaDirectInvestorsForm()
    return render(request, 'portal/idea_direct_investors.html', {'biz_invest_form': biz_invest_form,
                                                                 'dir_idea_investors_array': dir_idea_investors_array})


def idea_detail(request, id):
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    current_user_subscription = str(current_user_subscription.plan_category)
    team_members = []
    all_investors = []
    idea = get_object_or_404(Ideas, id=id)
    dir_idea_investors = idea.direct_idea_invest.all()
    dir_idea_investors_array = []
    for dir in dir_idea_investors:
        dir_idea_investors_array.append(dir.investor)
    user_profile = get_object_or_404(Profile, user=request.user)
    centinum = CentinumVentures.objects.all()
    centinum_count = centinum.count()
    ideas = Ideas.objects.all()
    ideas_count = ideas.count()
    startup = StartupBusiness.objects.all()
    startup_count = startup.count()
    investors = idea.invest_idea.filter(approved=True)
    investors_count = idea.invest_idea.filter(approved=True).count()
    idea_teams = idea.team_idea.all()
    for inv in investors:
        all_investors.append(inv.investor)
    for idea_mem in idea_teams:
        team_members.append(idea_mem.member)
    if request.method == 'POST':
        idea_form = IdeaForm(data=request.POST, instance=idea)
        if idea_form.is_valid():
            idea = idea_form.save(commit=False)
            idea.save()
            return redirect('account:profile')
    else:
        idea_form = IdeaForm(instance=idea)
    return render(request, 'portal/idea_detail.html', {'idea': idea,
                                                       'all_investors': all_investors,
                                                       'investors': investors,
                                                       'centinum': centinum,
                                                       'centinum_count': centinum_count,
                                                       'ideas': ideas,
                                                       'ideas_count': ideas_count,
                                                       'startup': startup,
                                                       'startup_count': startup_count,
                                                       'team_members': team_members,
                                                       'investors_count': investors_count,
                                                       'user_profile': user_profile,
                                                       'idea_form': idea_form,
                                                       'idea_teams': idea_teams,
                                                       'dir_idea_investors_array': dir_idea_investors_array,
                                                       'dir_idea_investors': dir_idea_investors,
                                                       'current_user_subscription': current_user_subscription})


@innovator_required
@login_required
def add_idea(request):
    if request.method == 'POST':
        idea_form2 = IdeaForm(data=request.POST)
        if idea_form2.is_valid():
            new_idea_form = idea_form2.save(commit=False)
            new_idea_form.user = request.user
            new_idea_form.save()
            return redirect('portal:profile')
    else:
        idea_form2 = IdeaForm()
    return render(request, 'portal/idea.html', {'idea_form2': idea_form2})


@innovator_required
@login_required
def edit_idea(request, id):
    idea = get_object_or_404(Ideas, id=id)
    if request.method == 'POST':
        idea_form = IdeaForm(data=request.POST, instance=idea)
        if idea_form.is_valid():
            idea = idea_form.save(commit=False)
            idea.save()
            return redirect('portal:innovator')
    else:
        idea_form = IdeaForm(instance=idea)
    return render(request, 'portal/edit_idea.html', {'idea_form': idea_form})


@entrepreneur_required
@login_required
def add_business(request):
    business_image_formset = modelformset_factory(BusinessImages,
                                                  form=BusinessImageForm, extra=3)
    if request.method == 'POST':
        business_form = BusinessForm(data=request.POST)
        formset = business_image_formset(request.POST, request.FILES,
                                         queryset=BusinessImages.objects.none())
        if business_form.is_valid() and formset.is_valid():
            new_business_form = business_form.save(commit=False)
            new_business_form.user = request.user
            new_business_form.save()
            for form in formset.cleaned_data:
                # this helps to not crash if the user
                # do not upload all the photos
                if form:
                    image = form['image']
                    photo = BusinessImages(business=business_form, image=image)
                    photo.save()
            return redirect('portal:entrepreneur')
    else:
        business_form = BusinessForm()
        formset = business_image_formset(queryset=BusinessImages.objects.none())
    return render(request, 'portal/business.html', {'business_form': business_form, 'formset': formset})


@entrepreneur_required
@login_required
def edit_business(request, id):
    business = get_object_or_404(StartupBusiness, id=id)
    if request.method == 'POST':
        business_form = BusinessForm(data=request.POST, instance=business)
        if business_form.is_valid():
            business = business_form.save(commit=False)
            business.save()
            messages.success(request, 'Updated successfully')
            return redirect('portal:entrepreneur')
        else:
            messages.error(request, 'Error updating the start up')
    else:
        business_form = BusinessForm(instance=business)
    return render(request, 'portal/edit_business.html', {'business_form': business_form})


def edit_partner(request):
    if request.method == 'POST':
        pat_edit_form = PartnersForm(data=request.POST)
        if pat_edit_form.is_valid():
            new_pat_form = pat_edit_form.save(commit=False)
            new_pat_form.save()
            return redirect('account:profile')
    else:
        pat_edit_form = PartnersForm()
    return render(request, 'account/profile.html', {'pat_edit_form': pat_edit_form})


@investor_required
@login_required
def investments(request):
    investments = IdeaInvestments.objects.filter(investor=request.user)
    investment_count = IdeaInvestments.objects.count()
    return render(request, 'portal/investments.html',
                  {'investments': investments, 'investment_count': investment_count})


@investor_required
def invest_idea(request, id):
    idea = get_object_or_404(Ideas, id=id)
    ideaInvest = IdeaInvestments()
    ideaInvest.idea = idea
    ideaInvest.investor = request.user
    ideaInvest.save()
    messages.success(request, "Request sent successfully")
    return redirect('account:profile')


@login_required
@investor_required
def investments_business(request):
    biz_investments = BusinessInvestments.objects.filter(investor=request.user)
    biz_investment_count = BusinessInvestments.objects.count()
    return render(request, 'portal/investment_biz.html',
                  {'investments': biz_investments, 'investment_count': biz_investment_count})


@investor_required
@login_required
def invest_business(request, id):
    busines = get_object_or_404(StartupBusiness, id=id)
    businesInvest = BusinessInvestments()
    businesInvest.business = busines
    businesInvest.investor = request.user
    businesInvest.save()
    messages.success(request, "Request sent successfully")
    return redirect('account:profile')


@login_required
def join_business(request, id):
    business = get_object_or_404(StartupBusiness, id=id)
    biz_team = BusinessTeams()
    biz_team.business = business
    biz_team.member = request.user
    biz_team.save()
    messages.success(request, "Joined team successfully")
    return redirect('account:profile')


@login_required
def join_idea(request, id):
    idea = get_object_or_404(Ideas, id=id)
    idea_team = IdeaTeams()
    idea_team.idea = idea
    idea_team.member = request.user
    idea_team.save()
    messages.success(request, "joined team successfully")
    return redirect('account:profile')


def terms(request):
    return render(request, 'portal/terms.html')


def privacy(request):
    return render(request, 'portal/privacy.html')


def plans(request):
    checker = False
    created_date = None
    due_date = None
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    sub_id = Subscriptions.objects.get(user_subscription=current_user_subscription)
    current_user_subscription = current_user_subscription.plan
    if sub_id.stripe_subscription_id is not None:
        sub_id = sub_id.stripe_subscription_id
        current_plan = stripe.Subscription.retrieve(sub_id)
        created_date = datetime.fromtimestamp(current_plan.created)
        due_date = datetime.fromtimestamp(current_plan.current_period_end)

        dif = due_date - created_date
        if str(dif) == '7 days, 0:00:00':
            checker = True
    plan_cats = PlanCategories.objects.all()
    return render(request, 'portal/plans.html', {'current_user_subscription': current_user_subscription,
                                                 'plan_cats': plan_cats,
                                                 'checker': checker,
                                                 'created_date': created_date,
                                                 'due_date': due_date})


def plan_startup_detail(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    plan_cat = PlanCategories.objects.get(name='Startup')
    plans = Plans.objects.filter(plan_category=plan_cat)
    return render(request, 'portal/plan_startup_detail.html', {'plans': plans,
                                                               'plan_cat': plan_cat,
                                                               'current_user_subscription': current_user_subscription,
                                                               'key': key
                                                               })


def plan_pro_detail(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    plan_cat = PlanCategories.objects.get(name='Pro')
    plans = Plans.objects.filter(plan_category=plan_cat)
    return render(request, 'portal/plan_pro_detail.html', {'plans': plans,
                                                           'plan_cat': plan_cat,
                                                           'current_user_subscription': current_user_subscription,
                                                           'key': key
                                                           })


def plan_ent_detail(request):
    key = settings.STRIPE_PUBLISHABLE_KEY
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    current_user_subscription = current_user_subscription.plan
    plan_cat = PlanCategories.objects.get(name='Enterprise')
    plans = Plans.objects.filter(plan_category=plan_cat)
    return render(request, 'portal/plan_ent_detail.html', {'plans': plans,
                                                           'plan_cat': plan_cat,
                                                           'current_user_subscription': current_user_subscription,
                                                           'key': key
                                                           })


class HomePageView(TemplateView):
    template_name = 'portal/stripe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request, id):
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    customer_id = current_user_subscription.stripe_customer_id
    current_user_subscription_id = Subscriptions.objects.get(user_subscription=current_user_subscription)
    if current_user_subscription_id.stripe_subscription_id is not None:
        current_user_subscription_id = current_user_subscription_id.stripe_subscription_id
    plan = Plans.objects.get(id=id)
    plan_id = plan.stripe_plan_id
    if request.method == 'POST':
        try:
            token = request.POST['stripeToken']
            # customer.source = token  # 4242424242424242
            # print("WAAAAA")
            # customer.save()
            stripe.Customer.create_source(
                customer_id,
                source=token
            )
            print(plan_id)
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[
                    {"plan": plan_id},
                ],
                trial_period_days=7
            )
            if subscription.status != "incomplete":
                if current_user_subscription_id is not None:
                    stripe.Subscription.delete(current_user_subscription_id)
                current_user_subscription.plan = plan
                current_user_subscription.save()
                current_subscription, created = Subscriptions.objects.get_or_create(user_subscription=current_user_subscription)
                current_subscription.stripe_subscription_id = subscription.id
                current_subscription.active = True
                current_subscription.save()
                return render(request, 'portal/success_sub.html')
            else:
                return redirect('portal:fail')

        except:
            return redirect('portal:fail')


def cancel_subscription(request):
    current_user_subscription = UserSubscriptions.objects.get(user=request.user)
    customer_id = current_user_subscription.stripe_customer_id
    current_user_sub_id = Subscriptions.objects.get(user_subscription=current_user_subscription)
    current_user_sub_id = current_user_sub_id.stripe_subscription_id
    stripe.Subscription.delete(current_user_sub_id)
    plan = Plans.objects.get(name='Free')
    subscription = stripe.Subscription.create(
        customer=customer_id,
        items=[
            {"plan": "plan_GAmCBtTCVEYk1T"},
        ],
    )

    current_user_subscription.plan = plan
    current_user_subscription.save()
    current_subscription, created = Subscriptions.objects.get_or_create(user_subscription=current_user_subscription)
    current_subscription.stripe_subscription_id = subscription.id
    current_subscription.active = True
    current_subscription.save()
    messages.success(request, "Subscription cancelled successfully. You now have the default free plan")
    return redirect('portal:plans')


def pay_for_service(request, id):
    service = Services.objects.get(id=id)
    charge = stripe.Charge.create(
        amount=service.service_cost * 100,
        currency='usd',
        description='Payment for Service',
        source=request.POST['stripeToken']
    )
    if charge.status == "succeeded":
        service.paid = True
        service.save()
        send_mail('Task Active', 'Hi {}!, your assigned task is now active. Check your tasks ASAP'.format(service.service_provider.username), 'centinum@gmail.com', [service.service_provider.email])
        messages.success(request, "Hi {}, your payment was successful".format(request.user.username))
        return redirect('account:profile')
    else:
        messages.error(request, "Hi {}", "Your payment was not successful.Please try again".format(request.user.username))
        return redirect('account:profile')


def pay_for_notes(request, id):
    note = PartnersPaymentNotes.objects.get(id=id)
    charge = stripe.Charge.create(
        amount=note.amount * 100,
        currency='usd',
        description='Payment for Service',
        source=request.POST['stripeToken']
    )
    if charge.status == "succeeded":
        note.paid = True
        note.save()
        messages.success(request, "Hi {}, your payment was successful".format(request.user.username))
        return redirect('account:profile')
    else:
        messages.error(request, "Hi {}", "Your payment was not successful.Please try again".format(request.user.username))
        return redirect('account:profile')


@csrf_exempt
def payment_done(request):
    profile = get_object_or_404(Profile, user=request.user)
    profile.paid = True
    profile.save()
    return render(request, 'portal/done.html')


@csrf_exempt
def payment_canceled(request):
    return render(request, 'portal/canceled.html')


def failed_subscription(request):
    return render(request, 'portal/sub_fail.html')


def paypal_process(request):
    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': '35',
        'currency_code': 'USD',
        'notify_url': 'http://{}{}'.format(host,
                                           reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host,
                                           reverse('portal:done')),
        'cancel_return': 'http://{}{}'.format(host,
                                              reverse('portal:canceled')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'portal/paypal.html', {'form': form})


def group_chat_view(request, id):
    business = get_object_or_404(StartupBusiness, id=id)
    group_chats = business.group_chats.all()

    if request.method == 'POST':
        group_form = GroupChatForm(request.POST)
        if group_form.is_valid():
            user_text = group_form.cleaned_data['message']
            user_text = user_text.lower()
            if 'money' in user_text or 'cash' in user_text or 'payment' in user_text:
                messages.error(request, 'Your text contains unwanted phrases')
            else:
                new_group = group_form.save(commit=False)
                new_group.business = business
                new_group.user = request.user
                new_group.save()
                group_form = GroupChatForm()

    else:
        group_form = GroupChatForm()
    return render(request, 'portal/group_chat.html',
                  {'group_chats': group_chats, 'group_form': group_form, 'business': business})


def group_chat_view_idea(request, id):
    idea = get_object_or_404(Ideas, id=id)
    group_chats = idea.group_chats_idea.all()

    if request.method == 'POST':
        group_form = GroupChatForm(request.POST)
        if group_form.is_valid():
            user_text = group_form.cleaned_data['message']
            user_text = user_text.lower()
            if 'money' in user_text or 'cash' in user_text or 'payment' in user_text:
                messages.error(request, 'Your text contains unwanted phrases')
            else:
                new_group = group_form.save(commit=False)
                new_group.idea = idea
                new_group.user = request.user
                new_group.save()
                group_form = GroupChatForm()

    else:
        group_form = GroupChatForm()
    return render(request, 'portal/group_chat_idea.html',
                  {'group_chats': group_chats, 'group_form': group_form, 'idea': idea})


def service_timeline_chat(request, id):
    service = get_object_or_404(Services, id=id)
    service_chats = service.service_chats.all()
    if request.method == 'POST':
        ser_chat_form = ServiceChat(request.POST)
        if ser_chat_form.is_valid():
            user_text = ser_chat_form.cleaned_data['message']
            user_text = user_text.lower()
            if 'money' in user_text or 'cash' in user_text or 'payment' in user_text:
                messages.error(request, 'Your text contains unwanted phrases')
            else:
                new_form = ser_chat_form.save(commit=False)
                new_form.service = service
                new_form.user = request.user
                new_form.save()
                send_mail('Comment Added',
                          '{} has added a comment on the {} timeline'.format(new_form.user, new_form.service),
                          'djangotest@gmail.com', [service.service_provider.email])

                ser_chat_form = ServiceChat()
    else:
        ser_chat_form = ServiceChat()
    return render(request, 'portal/service_chat.html', {'service_chats': service_chats, 'ser_chat_form': ser_chat_form,
                                                        'service': service})


def biz_user_search(request, id):
    business = get_object_or_404(StartupBusiness, id=id)
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = User.objects.exclude(username=request.user.username).annotate(
                search=SearchVector('username'),
            ).filter(search=query)
    return render(request,
                  'portal/biz_members_search.html',
                  {'form': form,
                   'query': query,
                   'results': results,
                   'business': business})


def idea_user_search(request, id):
    idea = get_object_or_404(Ideas, id=id)
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = User.objects.exclude(username=request.user.username).annotate(
                search=SearchVector('username'),
            ).filter(search=query)
    return render(request,
                  'portal/idea_members_search.html',
                  {'form': form,
                   'query': query,
                   'results': results,
                   'idea': idea,
                   })


def add_member_biz(request, id, user_id):
    business = get_object_or_404(StartupBusiness, id=id)
    user = get_object_or_404(User, id=user_id)
    biz_team = BusinessTeams()
    biz_team.business = business
    biz_team.member = user
    biz_team.save()
    return redirect('account:profile')


def add_member_idea(request, id, user_id):
    idea = get_object_or_404(Ideas, id=id)
    user = get_object_or_404(User, id=user_id)
    idea_team = IdeaTeams()
    idea_team.idea = idea
    idea_team.member = user
    idea_team.save()
    return redirect('account:profile')


def accept_idea_request(request, id):
    idea = get_object_or_404(IdeaInvestments, id=id)
    idea.approved = True
    idea.save()
    return redirect('account:profile')


def accept_biz_request(request, id):
    business = get_object_or_404(BusinessInvestments, id=id)
    business.approved = True
    business.save()
    return redirect('account:profile')


def decline_idea_request(request, id):
    idea = get_object_or_404(IdeaInvestments, id=id)
    idea.declined = True
    idea.save()
    return redirect('account:profile')


def decline_biz_request(request, id):
    business = get_object_or_404(BusinessInvestments, id=id)
    business.declined = True
    business.save()
    return redirect('account:profile')


def partner_notes(request):
    if request.method == 'POST':
        partner_notes_form = PartnersPaymentForm(data=request.POST)
        if partner_notes_form.is_valid():
            new_form = partner_notes_form.save(commit=False)
            new_form.partner = request.user
            new_form.save()
            return redirect('account:profile')
    else:
        partner_notes_form = PartnersPaymentForm()


def service_detail(request, id):
    service = get_object_or_404(CentinumServices, id=id)
    if request.method == 'POST':
        form = ServicesForm(data=request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.client = request.user
            new_form.service_name = service
            new_form.save()
            messages.success(request, "Request sent successful")
            return redirect('portal:request_sent')
        else:
            messages.error(request, "Request Not successful")
    return render(request, 'portal/service_detail.html', {'service': service})


def request_sent(request):
    return render(request, 'portal/request_sent.html')


def service_provider_requests(request, id):
    service = get_object_or_404(CentinumServices, id=id)
    all_services = CentinumServices.objects.all()
    my_service = Services()
    for all_s in all_services:
        if all_s.client == request.user and all_s.service_name == service:
            messages.error(request, "You have already requested this service")
        else:
            my_service.client = request.user
            my_service.service_name = service
            my_service.save()
            messages.success(request, "Request sent successful")
    return render(request, 'portal/service_detail.html')


def mark_finished_service(request, id):
    service = get_object_or_404(Services, id=id)
    if request.method == 'POST':
        rating_form = RatingsForm(data=request.POST)
        if rating_form.is_valid():
            new_form = rating_form.save(commit=False)
            new_form.s_provider = service.service_provider
            new_form.save()
            service.finished = True
            service.save()
            rating_form = RatingsForm()
            messages.success(request, "Successfully rated service provider and marked as finished")
        else:
            messages.error(request, 'error rating service_provider')
    else:
        rating_form = RatingsForm()
    return render(request, 'portal/rating.html', {'rating_form': rating_form})
