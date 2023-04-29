from django.shortcuts import render
from django.views import generic

from .models import Pojistenec, Uzivatel
from .forms import PojistenecForm, UzivatelForm, LoginForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

class PojistenecIndex(generic.ListView):

    template_name = "databaze_pojistencu/pojistenec_index.html" # cesta k templatu ze složky templates (je možné sdílet mezi aplikacemi)
    context_object_name = "pojištěnci" # pod tímto jménem budeme volat list objektů v templatu
    
# tato funkce nám získává seznam pojištěnců od největšího id (9,8,7...)
    def get_queryset(self):
        return Pojistenec.objects.all().order_by("prijmeni")

		
class CurrentPojistenecView(generic.DetailView):

    model = Pojistenec
    template_name = "databaze_pojistencu/pojistenec_detail.html"
	
    def get(self, request, pk):
        try:
            pojistenec = self.get_object()
        except:
            return redirect("pojistenec_index")
        return render(request, self.template_name, {"pojistenec" : pojistenec})
		
    def post(self, request, pk):
        if request.user.is_authenticated:
            if "edit" in request.POST:
                return redirect("edit_pojistenec", pk=self.get_object().pk)
            else:
                if not request.user.is_admin:
                    messages.info(request, "Nemáš práva pro smazání pojištěnce.")
                    return redirect(reverse("pojistenec_index"))
                else:
                    self.get_object().delete()
        return redirect(reverse("pojistenec_index"))
	
class VytvoritPojistenec(LoginRequiredMixin, generic.edit.CreateView):

    form_class = PojistenecForm
    template_name = "databaze_pojistencu/vytvorit_pojistenec.html"

    # Metoda pro GET request, zobrazí pouze formulář
    def get(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání pojištěnce.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    # Metoda pro POST request, zkontroluje formulář, pokud je validní vytvoří nový pojištěnec, pokud ne zobrazí formulář s chybovou hláškou
    def post(self, request):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro přidání pojištěnce.")
            return redirect(reverse("pojistenec_index"))			
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("pojistenec_index")
        return render(request, self.template_name, {"form":form})
		
class EditPojistenec(LoginRequiredMixin, generic.edit.CreateView):
    form_class = PojistenecForm
    template_name = "databaze_pojistencu/vytvorit_pojistenec.html"
	
    def get(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu pojištěnce.")
            return redirect(reverse("pojistenec_index"))
        try:
            pojistenec = Pojistenec.objects.get(pk = pk)
        except:
            messages.error(request, "Tento pojištěnec neexistuje!")
            return redirect("pojistenec_index")
        form = self.form_class(instance=pojistenec)
        return render(request, self.template_name, {"form":form})

    def post(self, request, pk):
        if not request.user.is_admin:
            messages.info(request, "Nemáš práva pro úpravu pojištěnce.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(request.POST)

        if form.is_valid():
            jmeno = form.cleaned_data["jmeno"]
            prijmeni = form.cleaned_data["prijmeni"]
            vek = form.cleaned_data ["vek"]
            pojisteni = form.cleaned_data["pojisteni"]
            detail_pojisteni = form.cleaned_data["detail_pojisteni"]
            try:
                pojistenec = Pojistenec.objects.get(pk = pk)
            except:
                messages.error(request, "Tento pojištěnec neexistuje!")
                return redirect(reverse("pojistenec_index"))
            pojistenec.jmeno = jmeno
            pojistenec.prijmeni = prijmeni
            pojistenec.vek = vek
            pojistenec.pojisteni = pojisteni
            pojistenec.detail_pojisteni.set(detail_pojisteni)
            pojistenec.save()
        #return render(request, self.template_name, {"form":form})
        return redirect("pojistenec_detail", pk = pojistenec.id)
		
class UzivatelViewRegister(generic.edit.CreateView):
    form_class = UzivatelForm
    model = Uzivatel
    template_name = "databaze_pojistencu/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("pojistenec_index"))            
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form":form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            uzivatel = form.save(commit = False)
            password = form.cleaned_data["password"]
            uzivatel.set_password(password)
            uzivatel.save()
            login(request, uzivatel)
            return redirect("pojistenec_index")
            
        return render(request, self.template_name, {"form":form})

class UzivatelViewLogin(generic.edit.CreateView):
    form_class = LoginForm
    template_name = "databaze_pojistencu/user_form.html"

    def get(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("pojistenec_index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("pojistenec_index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect("pojistenec_index")
            else:
                messages.error(request, "Tento účet neexistuje.")
        return render(request, self.template_name, {"form": form})
		
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "Nemůžeš se odhlásit, pokud nejsi přihlášený.")
    return redirect(reverse("login"))
