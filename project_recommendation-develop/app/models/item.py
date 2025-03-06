from settings import Color, Material, ClothingStyle, Size, Category


class Item:
    def __init__(self, item_id: int, discription: str, color: Color, material: Material, name: str, category: Category,
                 price: float):
        self.__item_id = item_id
        self.__name = name
        self.__discription = discription
        self.__color = color
        self.__material = material
        self.__category = category
        self.__price = price

    @property
    def item_id(self) -> int:
        return self.__item_id

    @property
    def discription(self) -> str:
        return self.__discription

    @property
    def material(self) -> Material:
        return self.__material

    @property
    def color(self) -> Color:
        return self.__color

    @property
    def name(self) -> str:
        return self.__name

    @property
    def category(self) -> Category:
        return self.__category

    @property
    def price(self) -> float:
        return self.__price


class ClothingItem(Item):
    def __init__(self, item_id: int, discription: str, color: Color, material: Material, name: str, category: Category,
                 price: float,
                 style: ClothingStyle, size: Size):
        super().__init__(item_id, discription, color, material, name, category, price)
        self.__style = style
        self.__size = size

    @property
    def style(self) -> ClothingStyle:
        return self.__style

    @property
    def size(self) -> Size:
        return self.__size

    @property
    def category(self) -> str:
        return f"Clothes: {super().category}"

    @property
    def clothes_category(self) -> Category:
        return super().category
