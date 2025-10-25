from datetime import datetime
from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.shortcuts import reverse

# import models used to build dashboard stats
from farm.models import Farm, SiteVisit, Notice, Statement, FarmEmployeeStats


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    """
    Dashboard view that shows top-level counts and a small carousel of active notices.

    Role scoping:
    - If the current user has role == 'Manager' (CustomUser.role), they see counts only for
      farms they own and related objects.
    - Other users see global counts.
    """
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs: Any):
        ctx = super().get_context_data(**kwargs)
        User = get_user_model()
        user = self.request.user

        # Determine farm scope: managers only see their own farms
        if getattr(user, 'role', None) == 'Manager':
            farm_qs = Farm.objects.filter(owner=user)
        else:
            farm_qs = Farm.objects.all()

        # Counts
        farms_count = farm_qs.count()
        users_count = User.objects.count()
        sitevisits_count = SiteVisit.objects.filter(farm__in=farm_qs).count()
        statements_count = Statement.objects.filter(farm__in=farm_qs).count()
        employee_stats_count = FarmEmployeeStats.objects.filter(farm__in=farm_qs).count()
        active_notices = Notice.objects.filter(is_active=True).order_by('-created')[:6]

        # Recent items (latest 5)
        recent_farms = farm_qs.order_by('-created')[:5]
        recent_visits = SiteVisit.objects.filter(farm__in=farm_qs).order_by('-visit_date')[:5]
        recent_statements = Statement.objects.filter(farm__in=farm_qs).order_by('-created')[:5]

        ctx.update({
            'counts': {
                'users': users_count,
                'farms': farms_count,
                'sitevisits': sitevisits_count,
                'statements': statements_count,
                'employee_stats': employee_stats_count,
            },
            'recent_farms': recent_farms,
            'recent_visits': recent_visits,
            'recent_statements': recent_statements,
            'active_notices': active_notices,
        })

        return ctx

