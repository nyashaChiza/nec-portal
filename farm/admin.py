from django.contrib import admin
from django.db import models
from django.http import HttpResponse
import csv

from .models import Farm, SiteVisit, Notice, Statement, FarmEmployeeStats

# List of models to register
MODELS = [Farm, SiteVisit, Notice, Statement, FarmEmployeeStats]


def export_as_csv_action(description="Export selected objects as CSV",
                         fields=None):
    """
    Returns an admin action which exports selected model instances as CSV.
    `fields` is iterable of field names; if None uses model._meta.fields.
    """
    def export_as_csv(modeladmin, request, queryset):
        model = modeladmin.model
        opts = model._meta
        field_names = list(fields) if fields else [f.name for f in opts.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename={opts.label_lower}.csv'
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = []
            for field in field_names:
                try:
                    val = getattr(obj, field)
                except Exception:
                    val = ''
                # For callable / related objects, try to stringify
                if callable(val):
                    try:
                        val = val()
                    except Exception:
                        val = str(val)
                row.append(val)
            writer.writerow(row)
        return response

    export_as_csv.short_description = description
    return export_as_csv


# Build inlines for models that have FK -> other models (specifically Farm)
inlines_for = {m: [] for m in MODELS}
for child in MODELS:
    for f in child._meta.get_fields():
        # Detect many-to-one (ForeignKey) pointing to one of our models
        related = getattr(f, 'related_model', None)
        if related in MODELS and getattr(f, 'many_to_one', False):
            parent = related
            inline_name = f"{child.__name__}Inline"
            inline = type(inline_name, (admin.TabularInline,), {
                'model': child,
                'extra': 0,
                'fields': [fld.name for fld in child._meta.fields if fld.editable][:6],
                'show_change_link': True,
            })
            inlines_for[parent].append(inline)


# Helper to pick sensible fields for list_display/search/list_filter
def pick_list_display(model, max_fields=6):
    fields = [f.name for f in model._meta.fields][:max_fields]
    # Ensure pk present
    if 'pk' not in fields and model._meta.pk.name not in fields:
        fields = [model._meta.pk.name] + fields
    return tuple(fields)


def pick_search_fields(model, max_fields: int = 6) -> tuple[str, ...]:
    # collect CharField/TextField names and limit to max_fields
    names = [f.name for f in model._meta.fields if isinstance(f, (models.CharField, models.TextField))]
    return tuple(names[:max_fields])


def pick_list_filter(model, max_fields=6):
    return tuple(
        f.name for f in model._meta.fields
        if isinstance(f, (models.BooleanField, models.DateField, models.DateTimeField, models.ForeignKey))
    )[:max_fields]


# Register each model with a generated ModelAdmin
for model in MODELS:
    list_display = pick_list_display(model)
    search_fields = pick_search_fields(model)
    list_filter = pick_list_filter(model)
    readonly_fields = tuple(
        f.name for f in model._meta.fields
        if isinstance(f, (models.DateTimeField,)) and getattr(f, 'auto_now_add', False)
    )

    admin_attrs = {
        'list_display': list_display,
        'search_fields': search_fields,
        'list_filter': list_filter,
        'readonly_fields': readonly_fields,
        'ordering': ('-pk',),
        'actions': [export_as_csv_action(fields=list_display)],
    }

    # Add inlines if any
    inlines = inlines_for.get(model)
    if inlines:
        admin_attrs['inlines'] = tuple(inlines)

    # Prepopulate slug if available
    slug_field = None
    for f in model._meta.fields:
        if f.name == 'slug' and isinstance(f, models.CharField):
            slug_field = f.name
            break
    if slug_field:
        admin_attrs['prepopulated_fields'] = {'slug': ('name',)}

    # Auto-assign owner if field exists and blank
    def make_save_model():
        def save_model(self, request, obj, form, change):
            if hasattr(obj, 'owner') and (not getattr(obj, 'owner', None)):
                try:
                    obj.owner = request.user
                except Exception:
                    pass
            super(self.__class__, self).save_model(request, obj, form, change)
        return save_model

    # Build ModelAdmin subclass
    admin_name = f"{model.__name__}Admin"
    admin_class = type(admin_name, (admin.ModelAdmin,), admin_attrs)

    # Attach save_model override only for models with 'owner' attribute
    if any(f.name == 'owner' for f in model._meta.fields):
        admin_class.save_model = make_save_model()

    # Finally register
    try:
        admin.site.register(model, admin_class)
    except admin.sites.AlreadyRegistered:
        # If already registered, unregister then register new admin
        admin.site.unregister(model)
        admin.site.register(model, admin_class)
