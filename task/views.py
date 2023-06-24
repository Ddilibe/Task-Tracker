from django.shortcuts import render, redirect
from task.models import User, Task
from django.views import generic
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError, FieldDoesNotExist
# Create your views here.

TRACK_USER = "task_tracker_user"


class UserView(generic.CreateView):
    template_name = "user.html"
    context_object_name = "useradd"
    fields = ['username']
    success_url = reverse_lazy('all_task', kwargs={'name':TRACK_USER})
    model = User

    def form_valid(self, request, *args, **kwargs):
        print("This is making sure that the form valid function runs")
        # Confirming that the user actually exists
        try:
            user = self.request.POST.get('username')
            user_exists =  User.objects.filter(username=user).exists()
            print(f"User exists in the database {user_exists}")
            if user_exists:
                self.request.session[TRACK_USER] = user
                self.request.session.save()
                return self.success_url
        except FieldDoesNotExist as e:
            print("This is the exception that occured.")
            return self.success_url
        except Exception as e:
            request.add_error(None, f"Save Error: {str(e)}")
            return self.form_invalid(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        return self.form_valid(form)

    def get_success_url(self):
        return reverse_lazy('all_task', kwargs={'name':self.user_dict()})

    def user_dict(self):
        return self.request.POST.get('username')


class UserCreateView(generic.CreateView):
    template_name = "user.html"
    context_object_name = "useradd"
    fields = ['username']
    success_url = reverse_lazy('user', kwargs={'name':TRACK_USER})
    model = User

    def form_valid(self, request, *args, **kwargs):
        # Confirming that the user actually exists
        try:
            user = self.request.POST.get('username')
            user_exists =  User.objects.filter(username=user).exists()
            if not user_exists:
                self.request.session[TRACK_USER] = user
                self.request.session.save()
                return super().form_valid(request, *args, **kwargs)
            raise FieldDoesNotExist("Field Doesn't exists")
        except FieldDoesNotExist as e:
            return redirect('new_user')
        except Exception as e:
            request.add_error(None, f"Save Error: {str(e)}")
            return self.form_invalid(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'name':self.user_dict()})

    def user_dict(self):
        return self.request.POST.get('username')



class UserDeleteView(generic.DeleteView):
    template_name = "user_delete.html"
    model = User
    success_url = reverse_lazy('new_user')

    def dispatch(self, request, *arg, **kwargs):
        if TRACK_USER not in request.session:
            return redirect('new_user')

        return super().dispatch(request, *arg, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TaskCreateView(generic.CreateView):
    template_name = "task_create_view.html"
    model = Task
    success_url = reverse_lazy('all_task', )
    fields = ['title', 'description', 'status', 'due_date']

    def dispatch(self, request, *arg, **kwargs):
        if TRACK_USER not in request.session:
            return redirect('all_task')

        return super().dispatch(request, *arg, **kwargs)


    def form_valid(self, form):
        try:
            user = self.request.session.get(TRACK_USER)
            self.confirm_user(user, "User session has expired")
            user = User.objects.get(username=user)
            self.confirm_user(user, "User doesn't exist")
            form.instance.user = user
            return super().form_valid(form)
        except ValidationError:
            return redirect('all_task')
        except Exception as e:
            form.add_error(None, f"Save Error: {str(e)}")
            return self.form_invalid(form)

    def confirm_user(self, user, message):
        if not user:
            raise ValidationError(message)

    def get_success_url(self, *args, **kwargs):
        return reverse_lazy('all_task', kwargs={"name":self.request.session.get(TRACK_USER)})

class TaskIndexView(generic.ListView):
    template_name = "task_list_view.html"
    context_object_name = "tasks_obj"
    paginate_by = 10
    model = Task
    # queryset = Task.objects.filter(user=TaskIndexView.request.session.get(TRACK_USER))

    def dispatch(self, request, *arg, **kwargs):
        if TRACK_USER not in request.session:
            return redirect('new_user')

        return super().dispatch(request, *arg, **kwargs)

    # def queryset(self, *args, **kwargs):
        # print(super().queryset(*args, **kwargs))
        # return self.get_queryset(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        print(self.kwargs)
        if user := self.request.session.get(TRACK_USER):
            if user_exists := User.objects.filter(username=user).exists():
                user = User.objects.get(username=user)
                queryset = Task.objects.filter(user=user)
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["sessionuser"] = self.request.session.get(TRACK_USER)
        return context

class TaskDetailView(generic.DetailView):
    template_name = "task_detailed_view.html"
    model = Task
    context_object_name = "taskdetail"

    def dispatch(self, request, *arg, **kwargs):
        if TRACK_USER not in request.session:
            return redirect('new_user')

        return super().dispatch(request, *arg, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class TaskDeleteView(generic.DeleteView):
    template_name = "task_delete_view.html"
    model = Task
    success_url = reverse_lazy('all_task')

    def dispatch(self, request, *arg, **kwargs):
        if TRACK_USER not in request.session:
            return redirect('new_user')

        return super().dispatch(request, *arg, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class TaskUpdateView(generic.UpdateView):
    template_name = "task_update_view.html"
    models = Task
    success_url = reverse_lazy('detail-tasks')

    def dispatch(self, request, *arg, **kwargs):
        if TRACK_USER not in request.session:
            return redirect('new_user')

        return super().dispatch(request, *arg, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def home_page(request):
    return render(request, "home.html")
