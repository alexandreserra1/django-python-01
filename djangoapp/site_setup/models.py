from django.db import models  # Importa o módulo models do Django, que contém as classes base para definir modelos.
from utils.model_validators import validate_png
from utils.images import resize_image

# Create your models here.

class MenuLink(models.Model):  # Define uma nova classe chamada MenuLink que herda de models.Model, tornando-a um modelo Django.
    class Meta:  # Meta é uma classe interna que define metadados sobre o modelo.
        verbose_name = 'Menu Link'  # Define um nome legível singular para o modelo.
        verbose_name_plural = 'Menu Links'  # Define um nome legível plural para o modelo.
        
    text = models.CharField(max_length=50)  # Define um campo de texto com um comprimento máximo de 50 caracteres.
    url_or_path = models.CharField(max_length=2048)  # Define um campo de texto com um comprimento máximo de 2048 caracteres.
    new_tab = models.BooleanField(default=False)  # Define um campo booleano com valor padrão False.
    site_setup = models.ForeignKey(
        'SiteSetup', on_delete=models.CASCADE, blank=True, null=True, default=None,
        )#chave de fora, ira herdar de sitesetup

    def __str__(self):  # Define o método __str__, que retorna uma representação legível do objeto.
        return self.text  # Retorna o valor do campo text como a representação legível do objeto.

class SiteSetup(models.Model):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=255)

    show_header = models.BooleanField(default=True)
    show_search = models.BooleanField(default=True)
    show_menu = models.BooleanField(default=True)
    show_description = models.BooleanField(default=True)
    show_pagination = models.BooleanField(default=True)
    show_footer = models.BooleanField(default=True)

    favicon = models.ImageField(
        upload_to='assets/favicon/%Y/%m',
        blank=True, default='',
        validators=[validate_png],
    )
    
    def save (self, *args, **kwargs):
        current_favicon_name = str(self.favicon.name)
        if current_favicon_name != 'favicon.png':
            self.favicon.name = 'favicon.png'
        super().save(*args, **kwargs)
        favicon_changed = False
        
        if self.favicon:
            favicon_changed =  current_favicon_name != self.favicon.name
            
        if favicon_changed:
            resize_image(self.favicon, 32)
        
    
    def __str__(self):
        return self.title