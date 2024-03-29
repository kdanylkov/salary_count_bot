from enum import Enum


class TreatemtTypes(Enum):
    CLASSIC_COSMETOLOGY = "Классическая косметология"
    APPARATUS_COSMETOLOGY = "Аппаратная косметология"
    LASER = "Лазер"
    COSMETICS = "Косметика/Украшения"
    ROLLER_MASSAGE = "Роликовый массаж"
    INJECTIONS = "Инъекцонные процедуры"
    OWN_COSMET = "Косметология (свои материалы)"
    OWN_INJECTIONS = "Инъекции (свои материалы)"


TYPES_LIST = [t.name for t in TreatemtTypes]
