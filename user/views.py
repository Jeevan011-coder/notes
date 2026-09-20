from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from .models import Profile
from django.contrib.auth import login
from .forms import RegisterForm, UserUpdateForm, ProfileUpdateForm

def register(request):
    """Create the account, log the user straight in, and land on the dashboard."""
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f'Welcome {user.username}, your account is ready.')
            return redirect('home')

        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, error)
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})


@login_required
def prof(request):
    try:
        user_profile = request.user.profile
    except ObjectDoesNotExist:
        user_profile = Profile.objects.create(user=request.user)    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,f'Your account has been updated')
            return redirect('prof')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form':u_form,
        'p_form': p_form

    }
    return render(request ,'user/prof.html',context)