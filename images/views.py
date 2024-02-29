from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCreateForm
from .models import Image

# Create your views here.

@login_required
def image_create(r):
    if r.method=='POST':
        form=ImageCreateForm(data=r.POST)
        if form.is_valid():
            cd=form.cleaned_data
            new_image=form.save(commit=False)
            new_image.user=r.user
            new_image.save()
            messages.success(r, 'Image is added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form=ImageCreateForm(data=r.GET)
    return render(r, 'images/create.html', {'form':form,
                                            "section":'images'})


def image_detail(r, id, slug):
    image=get_object_or_404(Image, id=id, slug=slug)
    return render(r, 'images/detail.html', {"section":"images", "image":image})
