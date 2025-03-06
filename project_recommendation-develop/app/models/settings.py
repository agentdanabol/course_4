from enum import Enum

EXECUTION_COST = 10.0


class Category(Enum):
    T_SHIRT = "T-shirt"
    JEANS = "Jeans"
    DRESS = "Dress"
    SUIT = "Suit"
    SKIRT = "Skirt"
    TROUSERS = "Trousers"
    BOOTS = "Boots"
    SNEAKERS = "Sneakers"
    SHOES = "Shoes"


class ClothingStyle(Enum):
    SPORTY = "Sporty "
    CASUAL = "Casual"
    CLASSIC = "Classic"
    STREETWEAR = "Streetwear"
    PUNK = "Punk"


class Size(Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


class Color(Enum):
    RED = "Red"
    GREEN = "Green"
    BLUE = "Blue"
    YELLOW = "Yellow"
    CYAN = "Cyan"
    MAGENTA = "Magenta"
    BLACK = "Black"
    WHITE = "White"
    GRAY = "Gray"
    ORANGE = "Orange"
    PURPLE = "Purple"
    BROWN = "Brown"
    PINK = "Pink"


class Material(Enum):
    COTTON = "Cottom"
    LINEN = "Linen"
    WOOL = "Wool"
    SILK = "Silk"
    POLYESTER = "Polyester"
    NYLON = "Nylon"
    LEATHER = "Leather"
    SUEDE = "Suede"
    DENIM = "Denim"
