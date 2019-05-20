from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm


# Create your views here.
# 
# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.add_message(
#                        request, messages.SUCCESS,
#                        f'User {username} created!')
#             return redirect('main_app:home')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'users/register.html', {'form':form})
