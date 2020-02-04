import telegram
from telegram import Update

from database import session
from users import User


def get_user_from_update(update: Update) -> User:
    user = session.query(User).filter_by(id=update.effective_user.id).first()

    if user is None:
        new_user = User(id=update.effective_user.id, username=update.effective_user.username)
        if new_user.username is None:
            new_user.username = str(new_user.id)
        session.add(new_user)
        session.commit()
        return new_user
    else:
        if (user.username == str(user.id) or user.username is None) and update.effective_user.username is not None:
            user.username = update.effective_user.username
            session.commit()

    return user

mwe_category_keyboard = [['All the words in “GIVE UP” are 👏 together'],
                         ['Some words in “GIVE UP” are 🙌 separated'],
                         ['“GIVE” and “UP” do not form a special meaning together ✋ 🤚.']]

mwe_category_keyboard_markup = telegram.ReplyKeyboardMarkup(mwe_category_keyboard)

review_type_keyboard = [['👍 I agree. Nice example for this category'],
                            ['👎 I do not like this example'],
                            ['⏭ Skip this one'],
                            ['😱 Quit reviewing']]
review_type_keyboard_markup = telegram.ReplyKeyboardMarkup(review_type_keyboard)

mwe_category_level_1_keyboard = [['“GIVE” and “UP” do form a special meaning together 🙌.'],
                                 ['“GIVE” and “UP” do NOT form a special meaning together ✋ 🤚.']]

mwe_category_level_1_keyboard_markup = telegram.ReplyKeyboardMarkup(mwe_category_level_1_keyboard)

mwe_category_level_2_keyboard = [['All the words in “GIVE UP” are 👏 together'],
                                 ['Some words in “GIVE UP” are 🙌 separated']]

mwe_category_level_2_keyboard_markup = telegram.ReplyKeyboardMarkup(mwe_category_level_2_keyboard)
