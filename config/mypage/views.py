from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render, redirect
from django.urls import reverse

from mypage.forms import ProfileForm, PetForm, DiaryForm
from mypage.models import Profile, Pet, Diary
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
    return render(request, 'mypage/profile.html', {'profile_form': profile_form})


@login_required
@transaction.atomic
def create_pet(request):
    if request.method == 'POST':
        pet_form = PetForm(request.POST, request.FILES)
        if pet_form.is_valid():
            pet = pet_form.save()
            pet.owner = request.user.profile
            pet.save()
            messages.success(request, 'Your pet info was successfully updated!')
            return redirect('mypage:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        pet_form = PetForm()
    return render(request, 'mypage/create_pet.html', {'pet_form': pet_form})


def email_update(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        new_email = request.POST['email_update']
        user.profile.email = new_email
        user.save()
        return redirect('mypage:profile')


def tel_update(request):
    if request.method == 'POST':
        user_id = request.user.id
        user = User.objects.get(pk=user_id)
        new_tel = request.POST['tel_update']
        user.profile.tel = new_tel
        user.save()
        return redirect('mypage:profile')


@login_required
def pet_info(request):
    pets = Pet.objects.filter(owner=request.user.profile)
    ctx = {
        'pets': pets
    }
    return render(request, 'mypage/pet_info.html', ctx)


@login_required
def diary(request):
    diaries = Diary.objects.filter(author=request.user.profile)
    ctx = {
        'diaries': diaries
    }
    return render(request, 'mypage/diary.html', ctx)


@login_required
@transaction.atomic
def create_diary(request):
    if request.method == 'POST':
        form = DiaryForm(request.POST, request.FILES)
        if form.is_valid():
            diary = form.save()
            diary.author = request.user.profile
            diary.save()
            return redirect(reverse('mypage:detail_diary', kwargs={'pk': diary.pk}))
    else:
        form = DiaryForm()
    return render(request, 'mypage/diary_create.html', {
        'form': form,
    })


@login_required
def detail_diary(request, pk):
    diary = Diary.objects.get(pk=pk)
    data = {
        'diary': diary
    }
    return render(request, 'mypage/diary_detail.html', data)


def favorites(request):
    return render(request, 'mypage/favorites.html')
