from django.shortcuts import render, redirect, HttpResponse
from account.forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active and user.is_verified:
                    login(request, user)
                    if request.user.is_investor:
                        return redirect('portal:home')
                    elif request.user.is_innovator:
                        return redirect('portal:home')
                    elif request.user.is_entrepreneur:
                        return redirect('portal:home')
                    elif request.user.is_partner:
                        return redirect('portal:home')
                    elif request.user.is_service_provider:
                        return redirect('portal:home')
                    elif request.user.is_superuser or request.user.is_staff:
                        return redirect('/admin/')
                else:
                    login(request, user)
                    return redirect('account:verify')
            else:
                messages.error(request, 'Your username and password didn\'t match. please try again')

    else:
        form = LoginForm()
    return render(request, 'loginApp/login.html', {'form': form})
