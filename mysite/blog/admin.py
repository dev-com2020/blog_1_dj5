from django.contrib import admin
from django import forms
from django.contrib.auth.models import User

from .models import Post, FavouritePost, Comment


# napisać klasę, która zmieni formularz w User - czyli pole wyszukiwania ustawi na email



class PostAdminForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 10,                    # Wysokość: 10 wierszy
                'cols': 50,                    # Szerokość: ~50 znaków
                'placeholder': 'Wpisz treść posta...',  # Tekst zastępczy
                'class': 'form-control',       # Klasa CSS (np. Bootstrap)
                'style': 'resize: vertical;',  # Styl CSS (tylko pionowy resize)
                'maxlength': 1000,             # Maks. 1000 znaków
                'required': True,              # Pole wymagane
                'id': 'post-body',             # Unikalne ID
                'data-max-chars': '1000',      # Dane dla JavaScript
            })
        }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    list_display_links = ['title', 'slug']
    list_editable = ['status']
    list_per_page = 25
    autocomplete_fields = ['author']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS
    search_help_text = "Wyszukaj posty po tytule lub treści"

# żeby zarejestować nowe zmiany, należy wyrejestrować Django'wy model
# admin.site.unregister(User)
#
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     search_fields = ['email']



    # Wyświetlanie kluczowych informacji w tabeli (list_display).
    # Filtrowanie i wyszukiwanie postów (list_filter, search_fields).
    # Automatyzację tworzenia pól (prepopulated_fields).
    # Optymalizację dla dużych danych (raw_id_fields).
    # Łatwą nawigację po datach (date_hierarchy).
    # Domyślne sortowanie (ordering).
    # Lepsze filtrowanie dzięki fasetkom (show_facets).

# @admin.register(FavouritePost)
# class FavouritePostAdmin(admin.ModelAdmin):
#     list_display = ['user','post','created']
#     list_filter = ['created','user']
#     search_fields = ['user__username','post__title']
#     date_hierarchy = 'created'
#     ordering = ['-created']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','post','created','active']
    list_filter = ['active','created','updated']
    search_fields = ['name','email','body']