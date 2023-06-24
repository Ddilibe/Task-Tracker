from django.urls import path
from task import views


urlpatterns = [
    path('', views.home_page, name="Home-Page"),
    path('enter/', views.UserView.as_view(), name="user"),
    path('new/', views.UserCreateView.as_view(), name="new_user"),
    path('<str:name>/', views.UserDeleteView.as_view(),  name="delete-user"),
    path('<str:name>/all/', views.TaskIndexView.as_view(), name="all_task"),
    path('<str:name>/new/', views.TaskCreateView.as_view(), name="create-tasks"),
    path('<str:name>/<int:pk>/', views.TaskDetailView.as_view(), name="detail-tasks"),
    path('<str:name>/<int:pk>/', views.TaskUpdateView.as_view(), name="update-tasks"),
    path('<str:name>/<int:pk>/', views.TaskDeleteView.as_view(), name="delete-tasks"),
]
