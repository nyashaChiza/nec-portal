from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse_lazy
from .models import CustomUser as User

from .form import UserForm


class UserListView(LoginRequiredMixin, generic.ListView):
    model = User
    template_name = "users/index.html"
    context_object_name = "users"
    paginate_by = 25

class UserCreateView(LoginRequiredMixin, generic.CreateView):
    model = User
    form_class = UserForm
    template_name = "users/create.html"
    success_url = reverse_lazy("user:user_list")

class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UserForm
    template_name = "users/update.html"
    success_url = reverse_lazy("user:user_list")

class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy("user:user_list")
    
    def get(self, request, *args, **kwargs):
        # perform delete immediately on GET (bypass confirm page)
        return self.post(request, *args, **kwargs)

@login_required
def profile_view(request):
    return render(request, 'account/profile.html', {'user': request.user})
