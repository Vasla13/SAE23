from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # URLs for Etudiant
    path('etudiants/', views.etudiant_list, name='etudiant_list'),
    path('etudiants/<int:pk>/', views.etudiant_detail, name='etudiant_detail'),
    path('etudiants/new/', views.etudiant_create, name='etudiant_create'),
    path('etudiants/<int:pk>/edit/', views.etudiant_update, name='etudiant_update'),
    path('etudiants/<int:pk>/delete/', views.etudiant_delete, name='etudiant_delete'),

    # URLs for UE
    path('ues/', views.ue_list, name='ue_list'),
    path('ues/<int:pk>/', views.ue_detail, name='ue_detail'),
    path('ues/new/', views.ue_create, name='ue_create'),
    path('ues/<int:pk>/edit/', views.ue_update, name='ue_update'),
    path('ues/<int:pk>/delete/', views.ue_delete, name='ue_delete'),

    # URLs for Ressource
    path('ressources/', views.ressource_list, name='ressource_list'),
    path('ressources/<int:pk>/', views.ressource_detail, name='ressource_detail'),
    path('ressources/new/', views.ressource_create, name='ressource_create'),
    path('ressources/<int:pk>/edit/', views.ressource_update, name='ressource_update'),
    path('ressources/<int:pk>/delete/', views.ressource_delete, name='ressource_delete'),

    # URLs for Enseignant
    path('enseignants/', views.enseignant_list, name='enseignant_list'),
    path('enseignants/<int:pk>/', views.enseignant_detail, name='enseignant_detail'),
    path('enseignants/new/', views.enseignant_create, name='enseignant_create'),
    path('enseignants/<int:pk>/edit/', views.enseignant_update, name='enseignant_update'),
    path('enseignants/<int:pk>/delete/', views.enseignant_delete, name='enseignant_delete'),

    # URLs for Examen
    path('examens/', views.examen_list, name='examen_list'),
    path('examens/<int:pk>/', views.examen_detail, name='examen_detail'),
    path('examens/new/', views.examen_create, name='examen_create'),
    path('examens/<int:pk>/edit/', views.examen_update, name='examen_update'),
    path('examens/<int:pk>/delete/', views.examen_delete, name='examen_delete'),

    # URLs for Note
    path('notes/', views.note_list, name='note_list'),
    path('notes/<int:pk>/', views.note_detail, name='note_detail'),
    path('notes/new/', views.note_create, name='note_create'),
    path('notes/<int:pk>/edit/', views.note_update, name='note_update'),
    path('notes/<int:pk>/delete/', views.note_delete, name='note_delete'),

    # URL for file upload
    path('upload/', views.upload_file, name='upload_file'),

    # URL for grade report
    path('grade_report/<int:pk>/', views.grade_report, name='grade_report'),
]
