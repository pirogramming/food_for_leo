from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect

from mypage.forms import ProfileForm


# def create_profile(request):
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.user = request.user
#             instance.save()
#             return redirect('mypage:profile')
#     else:
#         form = ProfileForm()
#     return render(request, 'mypage/img_upload.html', {'form': form})


@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('mypage:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'mypage/img_upload.html', {'profile_form': profile_form})


def name_update(request):
    pass


def favorites(request):
    return render(request, 'mypage/favorites.html')


def diary(request):
    return render(request, 'mypage/diary.html')
