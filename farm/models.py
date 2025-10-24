from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Farm(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="farms"
    )
    address = models.CharField(max_length=255)
    size_in_hectares = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    telephone = models.CharField(max_length=100, blank=True)
    account_number = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, blank=True)
    sector = models.CharField(max_length=100, choices=[("Agro", "Agro"), ("General Agriculture", "General Agriculture"), ("Horticulture", "Horticulture"), ("Kapenta", "Kapenta"), ("Timber", "Timber"), ("Tea & Coffee", "Tea & Coffee"), ("Sugarcane","Sugarcane")])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class SiteVisit(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    ]

    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="visits")
    agent = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="site_visits"
    )
    visit_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    resolution_notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Visit to {self.farm.name} on {self.visit_date}"


class Notice(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    issued_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="issued_notices"
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Notice: {self.title} ({self.farm.name})"


class Statement(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name="statements")
    period_start = models.DateField()
    period_end = models.DateField()
    total_sales = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Statement for {self.farm.name} ({self.period_start} - {self.period_end})"

    def save(self, *args, **kwargs):
        self.balance = self.total_sales - self.total_expenses
        super().save(*args, **kwargs)





class FarmEmployeeStats(models.Model):
    EMPLOYMENT_TYPES = [
        ("PERMANENT", "Permanent"),
        ("SEASONAL", "Seasonal"),
        ("CASUAL", "Casual"),
        ("FIXED_TERM", "Fixed Term"),
    ]

    farm = models.ForeignKey("farm.Farm", on_delete=models.CASCADE, related_name="employee_stats")
    reporting_month = models.DateField(help_text="The month this record applies to")
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPES)

    # 🧍 Employee numbers
    citizen_male = models.PositiveIntegerField(default=0)
    citizen_female = models.PositiveIntegerField(default=0)
    expatriate_male = models.PositiveIntegerField(default=0)
    expatriate_female = models.PositiveIntegerField(default=0)

    # 💰 Payroll information
    basic_pay_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    basic_pay_zwl = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # 🧾 Contributions
    employees_contribution_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employees_contribution_zwl = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    employers_contribution_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    employers_contribution_zwl = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    # 📊 Arrears and totals
    arrears_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    arrears_zwl = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_contribution_usd = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_contribution_zwl = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="added_employee_stats")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Farm Employee Stats"
        unique_together = ("farm", "reporting_month", "employment_type")

    def __str__(self):
        return f"{self.farm.name} - {self.employment_type} ({self.reporting_month.strftime('%B %Y')})"

    def save(self, *args, **kwargs):
        """
        Automatically calculate total contributions based on:
        - employee + employer contributions + arrears
        """
        self.total_contribution_usd = (
            self.employees_contribution_usd + self.employers_contribution_usd + self.arrears_usd
        )
        self.total_contribution_zwl = (
            self.employees_contribution_zwl + self.employers_contribution_zwl + self.arrears_zwl
        )
        super().save(*args, **kwargs)
