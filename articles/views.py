from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from .models import *

class BroCreateView(CreateView):
    model = Bro
    fields = ['body']
    template_name = 'bro.html'
    success_url = reverse_lazy('bro-create')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(BroCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print(form.errors)
        return redirect(reverse_lazy('bro-create'))

    def bro(self, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class PopCreateView(CreateView):
    model = Pop
    fields = ['body']
    template_name = 'popup.html'
    success_url = reverse_lazy('pop-create')

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        return super(BroCreateView, self).form_valid(form)

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        print(form.errors)
        return redirect(reverse_lazy('pop-create'))

    def bro(self, *args, **kwargs):
        form = self.get_form()
        self.object = None
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)