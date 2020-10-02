from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.urls import reverse

from .models import User
from .forms import RegistrationForm, EditForm, LoginForm

class IndexView(generic.TemplateView):
    template_name = "webprofile/index.html"
    form_class = LoginForm
    initial = {}

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid():
            #form.cleaned_data empty !? Using request POST instead
            results = User.objects.filter(email=request.POST['email'], password=request.POST['password'])
            if len(results) != 1:
                return render(request, self.template_name, {'form': form, 'error_message': 'Identifiants invalides'})

            response = HttpResponseRedirect(reverse('webprofile:userView'))
            response.set_cookie('user_id', results[0].pk)
            return response
        return render(request, self.template_name, {'form': form, 'error_message': 'Une erreur est survenue'})

# class RegisterView(generic.TemplateView):
#     template_name = "webprofile/inscription.html"

#     def get(self, request, *args, **kwargs):
#         return render(request, self.template_name)

#     def post(self, request, *args, **kwargs):

class UserView(generic.TemplateView):
    template_name = "webprofile/profil.html"
    form_class = EditForm
    initial = {}

    def get(self, request):
        try:
            user_id = request.COOKIES.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            print([user.email, user.password, user.favorite_food])
            return render(request, self.template_name, {'user': user})
        except:
            response = HttpResponseRedirect(reverse('webprofile:index'))
            return response
    def post(self, request):
        try:
            user_id = request.COOKIES.get('user_id')
            user = get_object_or_404(User, pk=user_id)
            print(user)
            # form = self.form_class(request.POST or None, instance=user)
            # if form.is_valid():
            # updated_user = form.save()
            # updated_user.save()
            user.email = request.POST['email']
            user.favorite_food = request.POST['favorite_food']
            user.save()
            response = HttpResponseRedirect(reverse('webprofile:userView'), {'user': user})
            return response
        except:
            return render(request, self.template_name, {'error_message': 'Une erreur est survenue'})


class RegisterFormView(View):
    form_class = RegistrationForm
    initial = {'email': '', 'password': '', 'favorite_food': ''}
    template_name = 'webprofile/inscription.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_user = form.save()
            print(new_user)
            response = HttpResponseRedirect(reverse('webprofile:userView'), {'user': new_user})
            response.set_cookie('user_id', new_user.pk)
            return response
        return render(request, self.template_name, {'form': form, 'error_message': 'Cet email est déjà utilisé.'})

class EditFormView(View):
    form_class = EditForm
    ##@TODO replace 1 with current user id
    initial = {'email': ''}
    template_name = 'webprofile/edition_profil.html'

    def get(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(User, request.COOKIES.get('user_id'))
            form = self.form_class(initial=user)
            return render(request, self.template_name, {'form': form})
        except:
            response = HttpResponseRedirect(reverse('webprofile:index'))
            return response
    

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, request.COOKIES.get('user_id'))
        form = self.form_class(initial=request.POST, instance=user)
        if form.is_valid():
            #@TODO: Save new email in DB
            new_user = form.save()
            return HttpResponse(new_user)
        return render(request, self.template_name, {'form': form})


def logout(request):
    response = HttpResponseRedirect(reverse('webprofile:index'))
    response.delete_cookie('user_id')
    return response