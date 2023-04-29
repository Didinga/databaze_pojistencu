from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class Pojisteni(models.Model):
    nazev_pojisteni = models.CharField(max_length=80, verbose_name="Pojištění")

    def __str__(self):
        return "{0}".format(self.nazev_pojisteni)

    class Meta:
        verbose_name="Pojištění"
        verbose_name_plural="Pojištění"
		
class Detail_pojisteni(models.Model):
    detail_pojisteni_title = models.CharField(max_length = 30, verbose_name="Detail_pojištění")

    def __str__(self):
        return self.detail_pojisteni_title

    class Meta:
        verbose_name = "Detail_pojištění"
        verbose_name_plural = "Detail_pojištění"		

class Pojistenec(models.Model):
    jmeno = models.CharField(max_length=200, verbose_name="Jméno")
    prijmeni = models.CharField(max_length=180, verbose_name="Příjmení")
    vek = models.CharField(max_length=180, default='', verbose_name="Věk")
    adresa = models.CharField(max_length=180, default='', verbose_name="Adresa")
    pojisteni = models.ForeignKey(Pojisteni, on_delete=models.SET_NULL, null=True, verbose_name="Druh pojištění")
    detail_pojisteni = models.ManyToManyField(Detail_pojisteni)
	
    def __init__(self, *args, **kwargs):
        super(Pojistenec, self).__init__(*args, **kwargs)
		
    def __str__(self):
        detail_pojisteni = [i.detail_pojisteni_title for i in self.detail_pojisteni.all()]
        return "Jmeno: {0} | Prijmeni: {1} | Vek: {2} | Adresa: {3} | Pojisteni: {4} | Detail_pojisteni: {5}".format(self.jmeno, self.prijmeni, self.vek, self.adresa, self.pojisteni.nazev_pojisteni, detail_pojisteni)

    class Meta:
        verbose_name="Pojištěnec"
        verbose_name_plural="Pojištěnci"
	
class UzivatelManager(BaseUserManager):
    # Vytvoří uživatele
    def create_user(self, email, password):
        print(self.model)
        if email and password:
            user = self.model(email=self.normalize_email(email))
            user.set_password(password)
            user.save()
        return user
    # Vytvoří admina
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_admin = True
        user.save()
        return user
		
class Uzivatel(AbstractBaseUser):

    email = models.EmailField(max_length = 300, unique=True)
    is_admin = models.BooleanField(default=False)

    class Meta:
        verbose_name = "uživatel"
        verbose_name_plural = "uživatelé"

    objects = UzivatelManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return "email: {}".format(self.email)
    
    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True	
