from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def entrepreneur_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='loginApp:login'):
    '''
    Decorator for views that checks that the logged in user is an entrepreneur,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_entrepreneur,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def investor_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='loginApp:login'):
    '''
    Decorator for views that checks that the logged in user is an investor,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_investor,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def innovator_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='loginApp:login'):
    '''
    Decorator for views that checks that the logged in user is an innovator,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_innovator,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def verification_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='loginApp:login'):
    '''
    Decorator for views that checks that the logged in user is an innovator,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_verified is True,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

