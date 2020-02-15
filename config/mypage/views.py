from django.shortcuts import render, redirect

from mypage.forms import ClientForm


def profile(request):
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('mypage:profile')
    else:
        form = ClientForm()
    return render(request, 'mypage/img_upload.html', {'form': form})


def name_update(request):
    pass


def pet_profile(request):
    return render(request, 'mypage/pet_profile.html')


def favorites(request):
    return render(request, 'mypage/favorites.html')


def diary(request):
    return render(request, 'mypage/diary.html')
