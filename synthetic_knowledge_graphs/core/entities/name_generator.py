from __future__ import annotations
from synthetic_knowledge_graphs.core.values.constants import EntityType


class NameGeneratorFRUNI:
    category_count = {}

    @classmethod
    def reset_counter(cls, category: EntityType | None = None):
        if category is None:
            cls.category_count = {}
        else:
            cls.category_count[category] = 0

    @classmethod
    def generate(
        cls, category: EntityType, uni_id=None, student_id=None, friend_id=None
    ):
        if category not in cls.category_count:
            cls.category_count[category] = 0

        uni_id = str(uni_id)
        student_id = str(student_id)
        friend_id = str(friend_id)

        name = str(category)
        if category == EntityType.UNIVERSITY:
            name_full = name + "-" + uni_id
        elif category == EntityType.STUDENT:
            name_full = name + "-" + uni_id + "-" + student_id
        elif category == EntityType.FRIEND:
            name_full = name + "-" + uni_id + "-" + student_id + "-" + friend_id
        else:
            raise ValueError("EntityType not supported")
        cls.category_count[category] += 1
        return name_full


class NameGeneratorFTREE:
    category_count = {}

    @classmethod
    def reset_counter(cls, category: EntityType | None = None):
        if category is None:
            cls.category_count = {}
        else:
            cls.category_count[category] = 0

    @classmethod
    def generate(cls, category: EntityType, tree_id=None, branch_id=None, kid_id=None):
        if category not in cls.category_count:
            cls.category_count[category] = 0

        name = str(category)
        tree_id = str(tree_id)
        branch_id = str(branch_id)
        kid_id = str(kid_id)
        if category == EntityType.PROGENITOR:
            name_full = name + "-" + tree_id
        elif category == EntityType.KID:
            name_full = name + "-" + tree_id + "-" + branch_id + "-" + kid_id
        elif category == EntityType.LAST_KID:
            name_full = name + "-" + tree_id + "-" + branch_id
        elif category == EntityType.HOBBIE:
            name_full = name + "-" + tree_id + "-" + branch_id
        else:
            raise ValueError("EntityType not supported")
        cls.category_count[category] += 1
        return name_full


class NameGeneratorUIA:
    category_count = {}

    @classmethod
    def reset_counter(cls, category: EntityType | None = None):
        if category is None:
            cls.category_count = {}
        else:
            cls.category_count[category] = 0

    @classmethod
    def generate(cls, category: EntityType):
        if category not in cls.category_count:
            cls.category_count[category] = 0

        name = str(category)
        id_ = str(cls.category_count[category])
        if category == EntityType.ITEM:
            name_full = name + "-" + id_
        elif category == EntityType.ATTRIBUTE:
            name_full = name + "-" + id_
        elif category == EntityType.USER:
            name_full = name + "-" + id_
        else:
            raise ValueError("EntityType not supported")
        cls.category_count[category] += 1
        return name_full
