ITEM_PRICES = {
    "A": 50,
    "B": 30,
    "C": 20,
    "D": 15,
    "E": 40,
    "F": 10,
    "G": 20,
    "H": 10,
    "I": 35,
    "J": 60,
    "K": 70,
    "L": 90,
    "M": 15,
    "N": 40,
    "O": 10,
    "P": 50,
    "Q": 30,
    "R": 50,
    "S": 20,
    "T": 20,
    "U": 40,
    "V": 50,
    "W": 20,
    "X": 17,
    "Y": 20,
    "Z": 21,
}


OFFERS = [
    {
        "product": "A",
        "quantity": 3,
        "price": 130,
    },
    {"product": "A", "quantity": 5, "price": 200},
    {"product": "B", "quantity": 2, "price": 45},
    {"product": "E", "quantity": 2, "free_product": "B"},
    {"product": "F", "quantity": 3, "free_product": "F"},
    {"product": "H", "quantity": 5, "price": 45},
    {"product": "H", "quantity": 10, "price": 80},
    {"product": "K", "quantity": 2, "price": 120},
    {"product": "N", "quantity": 3, "free_product": "M"},
    {"product": "P", "quantity": 5, "price": 200},
    {"product": "Q", "quantity": 3, "price": 80},
    {"product": "R", "quantity": 3, "free_product": "Q"},
    {"product": "U", "quantity": 4, "free_product": "U"},
    {"product": "V", "quantity": 2, "price": 90},
    {"product": "V", "quantity": 3, "price": 130},
    {"product": "S", "quantity": 1, "price": 45, "multibuy_with": ["T","X","Y","Z"]}
    {"product": "T", "quantity": 1, "price": 45, "multibuy_with": ["S","X","Y","Z"]}
    {"product": "X", "quantity": 1, "price": 45, "multibuy_with": ["T","S","Y","Z"]}
    {"product": "Y", "quantity": 1, "price": 45, "multibuy_with": ["T","X","S","Z"]}
    {"product": "Z", "quantity": 1, "price": 45, "multibuy_with": ["T","X","Y","S"]}


]


