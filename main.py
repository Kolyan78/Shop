import json
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    rating: float


@dataclass
class Category:
    name: str
    products: list


class Basket:
    def __init__(self, buy_products=None):
        self.buy_products = buy_products
        if self.buy_products == None:
            self.buy_products = []
        self.num_of_goods = 0
        self.total_price = 0

    def __repr__(self):
        return f"{self.buy_products}"

@dataclass()
class User:
    # def __init__(self, login, password):
    login: str
    password: str
    basket: list = Basket()


class Login:
    def __init__(self):
        self.f = None  # идентификатор для работы с файлом
        self.user_name = None  # имя пользователя
        self.user_pass = None  # пароль
        self.all_users = []  # Список для поиска пользователя, при запуске считывается из файла
        self.enter = False  # флаг показывающий вошел ли пользователь или нет
        self.num = None  # номер пользователя в списке

        with open("users.json") as self.f:
            self.all_users = json.load(self.f)

    def check_user(self, key, data):
        for _ in range(len(self.all_users)):
            if self.all_users[_][key] == data:
                self.num = _
                return True
        return False

    def check_login(self):
        if self.check_user("user", self.user_name) == False:
            return f"Не существует пользователя с именем {self.user_name}"
        if self.check_user("pass", self.user_pass) == False:
            return "Неверный пароль"
        self.enter = True
        return f"Здравствуйте, {self.user_name}!"


class Shop:
    list_of_categories = []  # Список катергорий
    n = None
    list_ = None

    """
        Метод для печати таблицы с товарами. Вызывается, когда надо показать список товаров или список купленных товаров.
    """
    @classmethod
    def print_table(cls, list_):
        cls.list_ = list_
        cls.n = 0
        print("=================================================\n"
              "| №  | Наименование товара | Цена     | Рейтинг |\n"
              "|====|=====================|==========|=========|")
        for _ in list_:
            cls.n += 1
            print(f"| {cls.n:02} | {_.name.ljust(19)} | {str(_.price).rjust(5)} р. | {str(_.rating).ljust(7)} |")
        print("=================================================")

    """
    Просто печатает разделительную линию
    """
    @classmethod
    def print_line(cls):
        print("*************************************************")


    """
    Печатает меню
    """
    @classmethod
    def print_menu(cls):
        Shop.print_line()
        print("1. Просмотр списка категорий товаров\n"
              "2. Просмотр корзины\n"
              "3. Покупка товаров, находящихся в корзине")
        Shop.print_line()


log = Login()
while not log.enter:
    log.user_name = input("Введите имя пользователя: ")
    log.user_pass = input("Введите пароль: ")
    Shop.print_line()
    print(log.check_login())
    user = User(log.user_name, log.user_pass)

"""
Читает из файла список товаров, и создает список категорий каждый элемент которого,
представляюет из себя объект Category и список входящих в него товаров
"""
with open("products.json", encoding='utf8') as f:
    products = json.load(f)
    cats = {}
for i in products:
    if i['category'] not in cats:
        cats.update({i['category']: [Product(i['name'], i['price'], i['rating'])]})
    else:
        cats.get(i['category']).append(Product(i['name'], i['price'], i['rating']))
for i in cats:
    Shop.list_of_categories.append(Category(i, cats[i]))


while log.enter == True:
    Shop.print_menu()
    option = int(input("Введите номер операции, или 0 для выхода: "))

    if option == 1:
        Shop.print_line()
        print("В наличии следующие категории товаров:")
        for i in range(len(Shop.list_of_categories)):
            print(f"  {i + 1} - {Shop.list_of_categories[i].name}")
        Shop.print_line()
        sub_option = int(input(f"Введите номер каталога 1 - {len(Shop.list_of_categories)}, или 0 для возврата: ")) - 1
        if 0 <= sub_option <= len(Shop.list_of_categories):
            Shop.print_line()
            print(f"Каталог: {Shop.list_of_categories[sub_option].name}")
            Shop.print_table(Shop.list_of_categories[sub_option].products)
            while True:
                sub_sub_option = int(input(f"Введите номер товара 1 - {Shop.n}"
                                           f" чтобы положить его в корзину, или 0 для возврата: "))
                if 1 <= sub_sub_option <= Shop.n:
                    user.basket.buy_products.append(Shop.list_of_categories[sub_option].products[sub_sub_option - 1])
                    user.basket.num_of_goods += 1
                    user.basket.total_price += Shop.list_of_categories[sub_option].products[sub_sub_option - 1].price
                    print("Товар добавлен в корзину")
                else:
                    break
    elif option == 2:
        if len(user.basket.buy_products) > 0:
            print("Содержимое корзины:")
            Shop.print_table(user.basket.buy_products)
            print(f"В корзине находится: {user.basket.num_of_goods} товаров,"
                  f" на сумму: {user.basket.total_price} рублей.")
            sub_option = int(input(f"Для удаления из корзины введите номер позиции от 1 до {user.basket.num_of_goods}"
                  f" или 0 для возврата: ")) - 1
            if 0 <= sub_option < user.basket.num_of_goods:
                user.basket.total_price -= user.basket.buy_products[sub_option].price
                user.basket.num_of_goods -= 1
                user.basket.buy_products.pop(sub_option)
        else:
            Shop.print_line()
            print("Корзина пуста")
    elif option == 3:
        if user.basket.num_of_goods == 0:
            Shop.print_line()
            print("Вы не можете купить товары, корзина пуста")
        else:
            print(f"\nВы приобрели товары в количестве: {user.basket.num_of_goods}"
                  f" на сумму {user.basket.total_price} рублей")
            user.basket.buy_products = []
            user.basket.num_of_goods = 0
            user.basket.total_price = 0
    elif option == 0:
        Shop.print_line()
        print(f"До свидания, {log.user_name}!")
        break
    else:
        Shop.print_line()
        print("Неверный номер операции")
