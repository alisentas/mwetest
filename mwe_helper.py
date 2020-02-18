from typing import List

from database import session
from mwe import Mwe


def get_todays_mwe(language: str) -> Mwe:
    if language == "en":
        mwe: Mwe = session.query(Mwe).filter(Mwe.name == "give up").first()

        if mwe is None:
            mwe = Mwe(name="give up",
                      meaning="cease making an effort; admit defeat",
                      language="en")
            session.add(mwe)
            session.commit()
            return mwe
        else:
            return mwe
    elif language == "tr":
        mwe: Mwe = session.query(Mwe).filter(Mwe.name == "başının etini yemek").first()

        if mwe is None:
            mwe = Mwe(name="başının etini yemek",
                      meaning="karşısındakini bezdirinceye, bıktırıncaya kadar sürekli konuşmak veya bir şeyler söylemek",
                      language="tr")
            session.add(mwe)
            session.commit()
            return mwe
        else:
            return mwe


def get_mwe_words(mwe: Mwe) -> str:
    return ", ".join(mwe.name.split(" "))
