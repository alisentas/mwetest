from typing import List

import telegram

from language import get_language_token, Tokens
from mwe import Mwe
from mwe_helper import get_mwe_words


def get_main_keyboard_markup(language: str):
    main_keyboard = [
        [get_language_token(language, Tokens.TODAYS_MWE), get_language_token(language, Tokens.SUBMIT)],
        [get_language_token(language, Tokens.REVIEW), get_language_token(language, Tokens.SUGGEST_MWE)],
        [get_language_token(language, Tokens.SHOW_SCOREBOARD), get_language_token(language, Tokens.CHANGE_LANGUAGE)],
    ]
    return telegram.ReplyKeyboardMarkup(main_keyboard)


def get_language_selection_keyboard_markup(language: str):
    language_change_keyboard = [
        [get_language_token(language, Tokens.LANGUAGE_ENGLISH)],
        [get_language_token(language, Tokens.LANGUAGE_TURKISH)],
    ]
    return telegram.ReplyKeyboardMarkup(language_change_keyboard)


def get_submit_category_1_keyboard_markup(language: str, mwe: Mwe):
    submit_category_1_keyboard = [
        [get_language_token(language, Tokens.FORM_SPECIAL_MEANING_TOGETHER) % get_mwe_words(mwe)],
        [get_language_token(language, Tokens.DOESNT_FORM_SPECIAL_MEANING_TOGETHER) % get_mwe_words(mwe)],
    ]
    return telegram.ReplyKeyboardMarkup(submit_category_1_keyboard)


def get_submit_category_2_keyboard_markup(language: str, mwe: Mwe):
    submit_category_2_keyboard = [
        [get_language_token(language, Tokens.WORDS_ARE_TOGETHER) % get_mwe_words(mwe)],
        [get_language_token(language, Tokens.WORDS_ARE_SEPARATED) % get_mwe_words(mwe)],
    ]
    return telegram.ReplyKeyboardMarkup(submit_category_2_keyboard)


def get_review_type_keyboard_keyboard_markup(language: str):
    review_type_keyboard = [
        [get_language_token(language, Tokens.AGREE_NICE_EXAMPLE)],
        [get_language_token(language, Tokens.DO_NOT_LIKE_EXAMPLE)],
        [get_language_token(language, Tokens.SKIP_THIS_ONE)],
        [get_language_token(language, Tokens.QUIT_REVIEWING)]
    ]
    return telegram.ReplyKeyboardMarkup(review_type_keyboard)
