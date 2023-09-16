from enum import Enum


class TreatemtTypes(Enum):
    CLASSIC_COSMETOLOGY = "Классическая косметология"
    APPARATUS_COSMETOLOGY = "Аппаратная косметология"
    LASER = "Лазер"
    COSMETICS = "Косметика"
    ROLLER_MASSAGE = "Роликовый массаж"
    INJECTIONS = "Инъекцонные процедуры"


TYPES_LIST = [t.name for t in TreatemtTypes]
