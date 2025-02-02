from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from .forms import LoginForm, UserRegistrationForm, UserEditForms, ProfileEditForm
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin



def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username = data['username'],
                                password = data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse("Muvaffaqiyatli Royhatdan otdingiz")
                else:
                    return HttpResponse("Royhatdan otishingiz kerak")
            else:
                return HttpResponse("Loginda hatolik bor")
            
    else:
        form = LoginForm()
        context = {
            'form':form
        }
        return render(request, 'account/login.html', context)
    
    
    
    
from django.core.exceptions import ObjectDoesNotExist
@login_required
def dashboard_view(request):
    user = request.user
    try:
        profil_info = Profile.objects.get(user=user)
    except ObjectDoesNotExist:
        profil_info = None  # Agar profil mavjud bo'lmasa, None bo'lishi kerak

    context = {
        'user': user,
        'profile': profil_info,
    }

    if profil_info is None:
        context['profile_message'] = 'Profil rasmi mavjud emas'

    return render(request, 'pages/user_profile.html', context)





from django.contrib.auth.views import PasswordResetView

class CustomPasswordResetView(PasswordResetView):
    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        # Email orqali yuborishdan oldin tiklash linkini olish
        reset_link = context['protocol'] + "://" + context['domain'] + context['url']
        print(f"Password reset link: {reset_link}")  # Linkni terminalga chiqarish
        # Emailni jo'natishni davom ettirish
        super().send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name)

def user_register(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data["password"])
            new_user.save()
            Profile.objects.create(user=new_user)  # Bu yerda new_user ishlatilishi kerak
            
            context = {
                "new_user": new_user
            }
            
            return render(request, 'account/register_done.html', context)
    else:
        user_form = UserRegistrationForm()
        
    context = {
        "user_form": user_form
    }
        
    return render(request, 'account/register.html', context)



class SingupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'account/register.html'
    
    
    
@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForms(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
            
    else:
        user_form = UserEditForms(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    return render(request, 'account/profile_edit.html', {"user_form":user_form, "profile_form":profile_form})



class EditUserView(LoginRequiredMixin,View):
    
    
    def get(self, request):
        user_form = UserEditForms(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
        return render(request, 'account/profile_edit.html', {"user_form":user_form, "profile_form":profile_form})
    
    def post(self, request):
        user_form = UserEditForms(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

