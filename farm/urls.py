from django.urls import path
from . import views


urlpatterns = [
    # Farm
    path('farms/', views.FarmListView.as_view(), name='farm_list'),
    path('farms/create/', views.FarmCreateView.as_view(), name='farm_create'),
    path('farms/<int:pk>/', views.FarmDetailView.as_view(), name='farm_detail'),
    path('farms/<int:pk>/update/', views.FarmUpdateView.as_view(), name='farm_update'),
    path('farms/<int:pk>/delete/', views.FarmDeleteView.as_view(), name='farm_delete'),

    # SiteVisit
    path('sitevisits/', views.SiteVisitListView.as_view(), name='sitevisit_list'),
    path('sitevisits/create/', views.SiteVisitCreateView.as_view(), name='sitevisit_create'),
    path('sitevisits/<int:pk>/', views.SiteVisitDetailView.as_view(), name='sitevisit_detail'),
    path('sitevisits/<int:pk>/update/', views.SiteVisitUpdateView.as_view(), name='sitevisit_update'),
    path('sitevisits/<int:pk>/delete/', views.SiteVisitDeleteView.as_view(), name='sitevisit_delete'),

    # Notice
    path('notices/', views.NoticeListView.as_view(), name='notice_list'),
    path('notices/create/', views.NoticeCreateView.as_view(), name='notice_create'),
    path('notices/<int:pk>/', views.NoticeDetailView.as_view(), name='notice_detail'),
    path('notices/<int:pk>/update/', views.NoticeUpdateView.as_view(), name='notice_update'),
    path('notices/<int:pk>/delete/', views.NoticeDeleteView.as_view(), name='notice_delete'),
    path('notices/<int:pk>/toggle-status/', views.NoticeStatusView.as_view(), name='notice_toggle_status'),

    # Statement
    path('statements/', views.StatementListView.as_view(), name='statement_list'),
    path('statements/create/', views.StatementCreateView.as_view(), name='statement_create'),
    path('statements/<int:pk>/', views.StatementDetailView.as_view(), name='statement_detail'),
    path('statements/<int:pk>/update/', views.StatementUpdateView.as_view(), name='statement_update'),
    path('statements/<int:pk>/delete/', views.StatementDeleteView.as_view(), name='statement_delete'),

    # FarmEmployeeStats
    path('farm-employee-stats/', views.FarmEmployeeStatsListView.as_view(), name='farmemployeestats_list'),
    path('farm-employee-stats/create/', views.FarmEmployeeStatsCreateView.as_view(), name='farmemployeestats_create'),
    path('farm-employee-stats/<int:pk>/', views.FarmEmployeeStatsDetailView.as_view(), name='farmemployeestats_detail'),
    path('farm-employee-stats/<int:pk>/update/', views.FarmEmployeeStatsUpdateView.as_view(), name='farmemployeestats_update'),
    path('farm-employee-stats/<int:pk>/delete/', views.FarmEmployeeStatsDeleteView.as_view(), name='farmemployeestats_delete'),
]