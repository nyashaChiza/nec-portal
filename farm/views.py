from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import generic
from django.conf import settings
from django.views import View
from farm.models import Farm, SiteVisit, Notice, Statement, FarmEmployeeStats
from farm.forms import FarmForm, StatementForm, SiteVisitForm, FarmEmployeeStatsForm, NoticeForm
from django.core.exceptions import FieldError


# Farm views
class FarmListView(generic.ListView):
    model = Farm
    template_name = "farm/farm_list.html"
    context_object_name = "farms"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        # Only show farms managed by this user if they’re a Manager
        if user.is_authenticated and user.role == "Manager":
            qs = qs.filter(owner=user)

        # Admins see all farms
        return qs


class FarmDetailView(generic.DetailView):
    model = Farm
    template_name = "farm/detail.html"
    context_object_name = "farm"


class FarmCreateView(generic.CreateView):
    model = Farm
    # only show model fields that are writable via the form; owner will be set to request.user
    form_class = FarmForm
    template_name = "farm/create.html"
    success_url = reverse_lazy("farm:farm_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class FarmUpdateView(generic.UpdateView):
    model = Farm
    form_class = FarmForm
    template_name = "farm/update.html"
    success_url = reverse_lazy("farm:farm_list")


class FarmDeleteView(generic.DeleteView):
    model = Farm
    success_url = reverse_lazy("farm:farm_list")

    def get(self, request, *args, **kwargs):
        # perform delete immediately on GET (bypass confirm page)
        return self.post(request, *args, **kwargs)


# SiteVisit views
class SiteVisitListView(generic.ListView):
    model = SiteVisit
    template_name = "visits/index.html"
    context_object_name = "site_visits"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        farm = self.request.GET.get("farm")
        if not farm:
            return qs

        # try PK first, then fallback to slug if present; if neither works, return unfiltered qs
        try:
            return qs.filter(farm_id=int(farm))
        except (ValueError, TypeError):
            try:
                return qs.filter(farm__slug=farm)
            except FieldError:
                return qs


class SiteVisitDetailView(generic.DetailView):
    model = SiteVisit
    template_name = "visits/detail.html"
    context_object_name = "sitevisit"


class SiteVisitCreateView(generic.CreateView):
    model = SiteVisit
    form_class = SiteVisitForm
    template_name = "visits/create.html"
    success_url = reverse_lazy("farm:sitevisit_list")


class SiteVisitUpdateView(generic.UpdateView):
    model = SiteVisit
    form_class = SiteVisitForm
    template_name = "visits/update.html"
    context_object_name = "sitevisit"
    success_url = reverse_lazy("farm:sitevisit_list")


class SiteVisitDeleteView(generic.DeleteView):
    model = SiteVisit
    success_url = reverse_lazy("farm:sitevisit_list")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


# Notice views
class NoticeListView(generic.ListView):
    model = Notice
    template_name = "notices/index.html"
    context_object_name = "notices"
    paginate_by = 20


class NoticeDetailView(generic.DetailView):
    model = Notice
    template_name = "notices/detail.html"
    context_object_name = "notice"


class NoticeCreateView(generic.CreateView):
    model = Notice
    form_class = NoticeForm
    template_name = "notices/create.html"
    success_url = reverse_lazy("farm:notice_list")


class NoticeUpdateView(generic.UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = "notices/update.html"
    success_url = reverse_lazy("farm:notice_list")


class NoticeDeleteView(generic.DeleteView):
    model = Notice
    success_url = reverse_lazy("farm:notice_list")

    def get(self, request, *args, **kwargs):
        # perform delete immediately on GET (bypass confirm page)
        return self.post(request, *args, **kwargs)
    
class NoticeDeleteView(generic.DeleteView):
    model = Notice
    success_url = reverse_lazy("farm:notice_list")

    def get(self, request, *args, **kwargs):
        # perform delete immediately on GET (bypass confirm page)
        return self.post(request, *args, **kwargs)

class NoticeStatusView(View):
    success_url = reverse_lazy("farm:notice_list")

    def get(self, request, *args, **kwargs):
        notice_id = kwargs.get("pk")
        notice = get_object_or_404(Notice, pk=notice_id)
        notice.is_active = not notice.is_active
        notice.save(update_fields=["is_active"])
        return redirect(self.success_url)
    
# Statement views
class StatementListView(generic.ListView):
    model = Statement
    template_name = "statements/index.html"
    context_object_name = "statements"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        farm = self.request.GET.get("farm")
        if not farm:
            return qs

        # try PK first, then fallback to slug if present; if neither works, return unfiltered qs
        try:
            return qs.filter(farm_id=int(farm))
        except (ValueError, TypeError):
            try:
                return qs.filter(farm__slug=farm)
            except FieldError:
                return qs


class StatementDetailView(generic.DetailView):
    model = Statement
    template_name = "statements/detail.html"
    context_object_name = "statement"


class StatementCreateView(generic.CreateView):
    model = Statement
    form_class = StatementForm
    template_name = "statements/create.html"
    success_url = reverse_lazy("farm:statement_list")



class StatementUpdateView(generic.UpdateView):
    model = Statement
    form_class = StatementForm
    template_name = "statements/update.html"
    success_url = reverse_lazy("farm:statement_list")


class StatementDeleteView(generic.DeleteView):
    model = Statement
    success_url = reverse_lazy("farm:statement_list")
    def get(self, request, *args, **kwargs):
        # perform delete immediately on GET (bypass confirm page)
        return self.post(request, *args, **kwargs)


# FarmEmployeeStats views
class FarmEmployeeStatsListView(generic.ListView):
    model = FarmEmployeeStats
    template_name = "employees/index.html"
    context_object_name = "farm_employee_stats"
    paginate_by = 20

    def get_queryset(self):
        qs = super().get_queryset()
        farm = self.request.GET.get("farm")
        if not farm:
            return qs

        # try PK first, then fallback to slug if present; if neither works, return unfiltered qs
        try:
            return qs.filter(farm_id=int(farm))
        except (ValueError, TypeError):
            try:
                return qs.filter(farm__slug=farm)
            except FieldError:
                return qs


class FarmEmployeeStatsDetailView(generic.DetailView):
    model = FarmEmployeeStats
    template_name = "employees/detail.html"
    context_object_name = "stat"


class FarmEmployeeStatsCreateView(generic.CreateView):
    model = FarmEmployeeStats
    form_class = FarmEmployeeStatsForm
    template_name = "employees/create.html"
    success_url = reverse_lazy("farm:farmemployeestats_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        # Filter farm options based on the logged-in user's role
        if user.is_authenticated:
            if user.role == "Manager":
                form.fields["farm"].queryset = user.farms.all()
            elif user.role == "Admin":
                form.fields["farm"].queryset = Farm.objects.all()
            else:
                form.fields["farm"].queryset = Farm.objects.none()  # restrict others

        return form



class FarmEmployeeStatsUpdateView(generic.UpdateView):
    model = FarmEmployeeStats
    form_class = FarmEmployeeStatsForm
    template_name = "employees/update.html"
    success_url = reverse_lazy("farm:farmemployeestats_list")

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        user = self.request.user

        # Filter farm options based on the logged-in user's role
        if user.is_authenticated:
            if user.role == "Manager":
                form.fields["farm"].queryset = user.farms.all()
            elif user.role == "Admin":
                form.fields["farm"].queryset = Farm.objects.all()
            else:
                form.fields["farm"].queryset = Farm.objects.none()  # restrict others

        return form



class FarmEmployeeStatsDeleteView(generic.DeleteView):
    model = FarmEmployeeStats
    template_name = "farm/farmemployeestats_confirm_delete.html"
    success_url = reverse_lazy("farm:farmemployeestats_list")



