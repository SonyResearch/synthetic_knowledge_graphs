from __future__ import annotations

from typing import Optional


class EntityType:
    ATTRIBUTE = "attr"
    FRIEND = "fr"
    HOBBIE = "ho"
    ITEM = "it"
    KID = "kid"
    LAST_KID = "lkid"
    PROGENITOR = "pr"
    STUDENT = "st"
    UNIVERSITY = "uni"
    USER = "user"


class Relation:
    ENROLLS = "enrolls"
    FRIEND_OF = "friend_of"
    COLLABORATES_WITH = "collaborates_with"
    ANCESTOR_OF = "ancestor_of"

    def SENTIMENT(branch_length: Optional[int] = None):
        if branch_length is None:
            return "sent"
        else:
            return f"sent_{branch_length}"

    HELD_BY = "held_by"
    BOUGHT_BY = "bought_by"
