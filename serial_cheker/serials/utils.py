menu = [
    {'name': 'Главная Страница', 'url': 'home-page'},
    {'name': 'Топ 10', 'url': 'top-10'},
    {'name': 'Добавить сериал', 'url': 'add-page'},

]

{'name': 'Регистрация', 'url': 'registation'},
{'name': 'Вход', 'url': 'login'},
{'name': 'Выход', 'url': 'logout'},


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        new_menu = menu.copy()
        if not self.request.user.is_authenticated:
            new_menu.pop(2)
        context['menu'] = new_menu
        return context
