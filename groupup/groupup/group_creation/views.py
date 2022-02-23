from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormView
from groupup.group_creation.forms import GroupCreateForm

class UserGroupCreateView(LoginRequiredMixin, FormView):
    """View for creating new groups."""

    http_method_names = ['get', 'post']
    form_class = GroupCreateForm
    template_name = "group_creation.html"

    def form_valid(self, form: GroupCreateForm):
        obj = form.save(self.request.user.groupupuser)
        self.success_url = obj.get_absolute_url()
        return super().form_valid(form)
