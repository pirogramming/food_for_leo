from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from mypage.forms import ProfileForm
from mypage.models import Profile
from django.contrib.auth.models import User


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('mypage:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'mypage/img_upload.html', {'profile_form': profile_form})


def email_update(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        new_email = request.POST['email_update']
        user.profile.email = new_email
        user.save()
        return redirect('mypage:profile')



def favorites(request):
    return render(request, 'mypage/favorites.html')


def diary(request):
    return render(request, 'mypage/diary.html')
