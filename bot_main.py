import random
from collections import defaultdict

import telegram
from sqlalchemy import and_
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import mwe_helper
from bot_helpers import get_user_from_update
from submission import Submission
from database import session
from keyboard import get_main_keyboard_markup, get_language_selection_keyboard_markup, \
    get_submit_category_1_keyboard_markup, get_submit_category_2_keyboard_markup, \
    get_review_type_keyboard_keyboard_markup
from language import get_language_token, Tokens, get_random_congrats_message
from users import User
import key
from mwe_helper import get_mwe_words
from reviews import Review, POSITIVE_REVIEW, NEGATIVE_REVIEW, NEUTRAL_REVIEW

updater = Updater(key.TELEGRAM_API_KEY, use_context=True)
dispatcher = updater.dispatcher
bot = dispatcher.bot


def send_message_to_user(user: User, msg: str) -> None:
    try:
        bot.send_message(chat_id=user.id,
                         text=msg,
                         parse_mode=telegram.ParseMode.MARKDOWN)
    except:
        print("chat not found")


def start(update: Update, context: CallbackContext):
    user = get_user_from_update(update)

    if "state" in context.user_data:
        del context.user_data["state"]
    if "submission" in context.user_data:
        del context.user_data["submission"]

    update.message.reply_text(
        get_language_token(user.language, Tokens.WELCOME_MESSAGE) % user.username,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard_markup(user.language))


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def add_user(name: str, lang: str) -> User:
    user = User(
        id=random.randint(1, 10000),
        username=name,
        language=lang
    )
    session.add(user)
    session.commit()
    return user


def add_submission_by_user(user: User, subm: str, cat: str, lang: str) -> Submission:
    submission = Submission(
        user=user,
        value=subm,
        category=cat,
        language=lang,
        mwe=mwe_helper.get_todays_mwe(lang)
    )
    session.add(submission)
    session.commit()
    return submission


def add_review_by_user(user: User, submisson: Submission, review_type: int) -> None:
    review = Review(
        user=user,
        submission=submisson,
        review_type=review_type,
        mwe=mwe_helper.get_todays_mwe(user.language)
    )
    session.add(review)
    session.commit()
    pass


def load_test_data(update: Update, context: CallbackContext):
    user = get_user_from_update(update)

    turkan_s = add_user("turkan.s", "tr")
    gordon_f = add_user("gordon.f", "en")
    michael_j = add_user("michael.j", "en")
    elvis_p = add_user("elvis.p", "en")
    david_b = add_user("david.b", "en")
    donald_t = add_user("donald.t", "en")
    tarik_a = add_user("tarik.a", "tr")
    kemal_s = add_user("kemal.s", "tr")
    munir_o = add_user("munir.o", "tr")
    zeki_a = add_user("zeki.a", "tr")

    submission1 = add_submission_by_user(turkan_s, "İşte şimdi ayvayı yedim.", "together", "tr")
    submission2 = add_submission_by_user(gordon_f, "Will you give up please?", "together", "en")
    submission3 = add_submission_by_user(michael_j, "I finally gave up smoking.", "together", "en")
    submission4 = add_submission_by_user(elvis_p, "Give up now, you're not going to win this fight?", "together", "en")
    submission5 = add_submission_by_user(david_b, "They will not give that up to me?", "non-mwe", "en")
    submission6 = add_submission_by_user(donald_t, "Please give this up?", "separated", "en")
    submission7 = add_submission_by_user(tarik_a, "Ayvayı yedikten sonra doydum.", "non-mwe", "tr")
    submission8 = add_submission_by_user(kemal_s, "Ayvayı iyi yedik.", "separated", "tr")
    submission9 = add_submission_by_user(munir_o, "Ayvayı yedik yine.", "together", "tr")
    submission10 = add_submission_by_user(zeki_a, "Ayva ayva söyle bana, benden güzeli var mı dünyada?", "together", "tr")

    add_review_by_user(turkan_s, submission7, POSITIVE_REVIEW)
    add_review_by_user(turkan_s, submission8, POSITIVE_REVIEW)
    add_review_by_user(turkan_s, submission9, POSITIVE_REVIEW)
    add_review_by_user(turkan_s, submission10, NEGATIVE_REVIEW)
    add_review_by_user(tarik_a, submission1, POSITIVE_REVIEW)
    add_review_by_user(tarik_a, submission8, POSITIVE_REVIEW)
    add_review_by_user(tarik_a, submission9, POSITIVE_REVIEW)
    add_review_by_user(tarik_a, submission10, NEGATIVE_REVIEW)
    add_review_by_user(kemal_s, submission7, POSITIVE_REVIEW)
    add_review_by_user(kemal_s, submission1, POSITIVE_REVIEW)
    add_review_by_user(kemal_s, submission9, POSITIVE_REVIEW)
    add_review_by_user(kemal_s, submission10, NEGATIVE_REVIEW)
    add_review_by_user(munir_o, submission7, POSITIVE_REVIEW)
    add_review_by_user(munir_o, submission8, POSITIVE_REVIEW)
    add_review_by_user(munir_o, submission1, POSITIVE_REVIEW)
    add_review_by_user(munir_o, submission10, NEGATIVE_REVIEW)
    add_review_by_user(zeki_a, submission7, NEGATIVE_REVIEW)
    add_review_by_user(zeki_a, submission8, NEGATIVE_REVIEW)
    add_review_by_user(zeki_a, submission9, NEGATIVE_REVIEW)
    add_review_by_user(zeki_a, submission1, NEGATIVE_REVIEW)
    add_review_by_user(gordon_f, submission3, POSITIVE_REVIEW)
    add_review_by_user(gordon_f, submission4, POSITIVE_REVIEW)
    add_review_by_user(gordon_f, submission5, POSITIVE_REVIEW)
    add_review_by_user(gordon_f, submission6, POSITIVE_REVIEW)
    add_review_by_user(michael_j, submission2, POSITIVE_REVIEW)
    add_review_by_user(michael_j, submission4, POSITIVE_REVIEW)
    add_review_by_user(michael_j, submission5, POSITIVE_REVIEW)
    add_review_by_user(michael_j, submission6, POSITIVE_REVIEW)
    add_review_by_user(elvis_p, submission3, POSITIVE_REVIEW)
    add_review_by_user(elvis_p, submission2, POSITIVE_REVIEW)
    add_review_by_user(elvis_p, submission5, POSITIVE_REVIEW)
    add_review_by_user(elvis_p, submission6, POSITIVE_REVIEW)
    add_review_by_user(david_b, submission3, POSITIVE_REVIEW)
    add_review_by_user(david_b, submission4, POSITIVE_REVIEW)
    add_review_by_user(david_b, submission2, POSITIVE_REVIEW)
    add_review_by_user(david_b, submission6, POSITIVE_REVIEW)
    add_review_by_user(donald_t, submission3, POSITIVE_REVIEW)
    add_review_by_user(donald_t, submission4, POSITIVE_REVIEW)
    add_review_by_user(donald_t, submission5, POSITIVE_REVIEW)
    add_review_by_user(donald_t, submission6, POSITIVE_REVIEW)

    update.message.reply_text(
        get_language_token(user.language, Tokens.WELCOME_MESSAGE) % user.username,
        parse_mode=telegram.ParseMode.MARKDOWN,
        reply_markup=get_main_keyboard_markup(user.language))


load_test_data_handler = CommandHandler('load_test_data', load_test_data)
dispatcher.add_handler(load_test_data_handler)


def todays_mwe_handler(user: User, update: Update, context: CallbackContext):
    todays_mwe = mwe_helper.get_todays_mwe(user.language)
    update.message.reply_text(get_language_token(user.language, Tokens.TODAYS_MWE_REPLY_TEXT) % (todays_mwe.name, todays_mwe.meaning),
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=get_main_keyboard_markup(user.language))


def language_change_handler(user: User, update: Update, context: CallbackContext):
    context.user_data["state"] = "changing_language"
    update.message.reply_text(get_language_token(user.language, Tokens.SELECT_LANGUAGE),
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=get_language_selection_keyboard_markup(user.language))


def language_update_handler(user: User, update: Update, context: CallbackContext):
    if update.message.text == get_language_token(user.language, Tokens.LANGUAGE_ENGLISH):
        user.language = "en"
        session.commit()
        del context.user_data["state"]
        update.message.reply_text(get_language_token(user.language, Tokens.LANGUAGE_CHANGE_SUCCESSFUL),
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=get_main_keyboard_markup(user.language))
    elif update.message.text == get_language_token(user.language, Tokens.LANGUAGE_TURKISH):
        user.language = "tr"
        session.commit()
        del context.user_data["state"]
        update.message.reply_text(get_language_token(user.language, Tokens.LANGUAGE_CHANGE_SUCCESSFUL),
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=get_main_keyboard_markup(user.language))
    else:
        update.message.reply_text(get_language_token(user.language, Tokens.PLEASE_SELECT_VALID_LANGUAGE),
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=get_language_selection_keyboard_markup(user.language))


def submit_handler(user: User, update: Update, context: CallbackContext):
    todays_mwe = mwe_helper.get_todays_mwe(user.language)
    update.message.reply_text(get_language_token(user.language, Tokens.PLEASE_ENTER_EXAMPLE) % todays_mwe.name,
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=telegram.ReplyKeyboardRemove())
    context.user_data["state"] = "submit_example"


def submit_handler_2(user: User, update: Update, context: CallbackContext):
    todays_mwe = mwe_helper.get_todays_mwe(user.language)
    submission = Submission(value=update.message.text)
    context.user_data["submission"] = submission
    context.user_data["state"] = "submit_example_type_1"
    update.message.reply_text(get_language_token(user.language, Tokens.SPECIAL_MEANING) % todays_mwe.name,
                              parse_mode=telegram.ParseMode.MARKDOWN,
                              reply_markup=get_submit_category_1_keyboard_markup(user.language, todays_mwe))


def submit_handler_3(user: User, update: Update, context: CallbackContext):
    todays_mwe = mwe_helper.get_todays_mwe(user.language)

    submit_category_1_submissions = [
        get_language_token(user.language, Tokens.FORM_SPECIAL_MEANING_TOGETHER) % get_mwe_words(todays_mwe),
        get_language_token(user.language, Tokens.DOESNT_FORM_SPECIAL_MEANING_TOGETHER) % get_mwe_words(todays_mwe),
    ]

    if update.message.text in submit_category_1_submissions:
        if update.message.text == submit_category_1_submissions[0]:
            update.message.reply_text(get_language_token(user.language, Tokens.ARE_WORDS_SEPARATED) % get_mwe_words(todays_mwe),
                                      parse_mode=telegram.ParseMode.MARKDOWN,
                                      reply_markup=get_submit_category_2_keyboard_markup(user.language, todays_mwe))
            context.user_data["state"] = "submit_example_type_2"
        else:
            submission = context.user_data["submission"]
            submission.category = "non-mwe"
            submission.users_who_reviewed = ''
            submission.user = user
            submission.language = user.language
            submission.mwe = todays_mwe
            session.add(submission)
            session.commit()
            del context.user_data["state"]
            del context.user_data["submission"]
            update.message.reply_text(
                get_language_token(user.language, Tokens.THANKS_FOR_SUBMISSION) % (get_random_congrats_message(user.language), 30),
                parse_mode=telegram.ParseMode.MARKDOWN,
                reply_markup=get_main_keyboard_markup(user.language)
            )
    else:
        update.message.reply_text(
            get_language_token(user.language, Tokens.ENTER_VALID_MWE_CATEGORY_1),
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=get_submit_category_1_keyboard_markup(user.language, todays_mwe)
        )


def submit_handler_4(user: User, update: Update, context: CallbackContext):
    todays_mwe = mwe_helper.get_todays_mwe(user.language)

    submit_category_1_submissions = [
        get_language_token(user.language, Tokens.WORDS_ARE_TOGETHER) % get_mwe_words(todays_mwe),
        get_language_token(user.language, Tokens.WORDS_ARE_SEPARATED) % get_mwe_words(todays_mwe),
    ]

    if update.message.text in submit_category_1_submissions:
        submission: Submission = context.user_data["submission"]
        if update.message.text == get_language_token(user.language, Tokens.WORDS_ARE_TOGETHER) % get_mwe_words(todays_mwe):
            submission.category = "together"
        elif update.message.text == get_language_token(user.language, Tokens.WORDS_ARE_SEPARATED) % get_mwe_words(todays_mwe):
            submission.category = "separated"
        submission.user = user
        submission.language = user.language
        submission.mwe = todays_mwe
        session.add(submission)
        session.commit()
        del context.user_data["submission"]
        del context.user_data["state"]
        if update.message.text == get_language_token(user.language, Tokens.WORDS_ARE_TOGETHER) % get_mwe_words(todays_mwe):
            update.message.reply_text(
                get_language_token(user.language, Tokens.THANKS_FOR_SUBMISSION) % (get_random_congrats_message(user.language), 10),
                parse_mode=telegram.ParseMode.MARKDOWN,
                reply_markup=get_main_keyboard_markup(user.language)
            )
        elif update.message.text == get_language_token(user.language, Tokens.WORDS_ARE_SEPARATED) % get_mwe_words(todays_mwe):
            update.message.reply_text(
                get_language_token(user.language, Tokens.THANKS_FOR_SUBMISSION) % (get_random_congrats_message(user.language), 10),
                parse_mode=telegram.ParseMode.MARKDOWN,
                reply_markup=get_main_keyboard_markup(user.language)
            )
    else:
        update.message.reply_text(
            get_language_token(user.language, Tokens.ENTER_VALID_MWE_CATEGORY_1),
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=get_submit_category_2_keyboard_markup(user.language, todays_mwe)
        )


def user_not_in_reviewers(submission: Submission, user: User) -> bool:
    all_reviewer_names = [x.user.username for x in submission.reviews]
    return user.username not in all_reviewer_names


def review_handler(user: User, update: Update, context: CallbackContext):
    submissions = session.query(Submission).filter(and_(Submission.user_id != user.id, Submission.language == user.language)).all()
    submissions = sorted(submissions, key=lambda x: x.review_count, reverse=True)
    submissions = [x for x in submissions if user_not_in_reviewers(x, user)]

    if len(submissions) > 0:
        todays_mwe = mwe_helper.get_todays_mwe(user.language)
        submission = submissions[0]

        submission_category_messages = {
            "together": get_language_token(user.language, Tokens.FORM_SPECIAL_MEANING_TOGETHER) % get_mwe_words(todays_mwe),
            "separated": get_language_token(user.language, Tokens.ARE_WORDS_SEPARATED) % get_mwe_words(todays_mwe),
            "non-mwe": get_language_token(user.language, Tokens.DOESNT_FORM_SPECIAL_MEANING_TOGETHER) % get_mwe_words(todays_mwe)
        }

        context.user_data["state"] = "review"
        context.user_data['submission'] = submission

        reply_message = get_language_token(user.language, Tokens.REVIEW_MESSAGE) % (submission.value, submission_category_messages[submission.category])
        update.message.reply_text(reply_message,
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=get_review_type_keyboard_keyboard_markup(user.language))
    else:
        if "state" in context.user_data:
            del context.user_data["state"]
        update.message.reply_text(
            get_language_token(user.language, Tokens.NO_EXAMPLES_TO_REVIEW),
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard_markup(user.language)
        )


def review_handler_2(user: User, update: Update, context: CallbackContext):
    review_types = [
        get_language_token(user.language, Tokens.AGREE_NICE_EXAMPLE),
        get_language_token(user.language, Tokens.DO_NOT_LIKE_EXAMPLE),
        get_language_token(user.language, Tokens.SKIP_THIS_ONE),
        get_language_token(user.language, Tokens.QUIT_REVIEWING)
    ]
    user = get_user_from_update(update)

    if update.message.text in review_types:
        submission = context.user_data["submission"]
        todays_mwe = mwe_helper.get_todays_mwe(user.language)

        points_earned_for_submission = {
            "together": 10,
            "separated": 20,
            "non-mwe": 30
        }

        if update.message.text == review_types[0]:
            points_earned = points_earned_for_submission[submission.category]
            reply_message = get_language_token(user.language, Tokens.SOMEONE_LOVED_YOUR_EXAMPLE) % (get_random_congrats_message(user.language), points_earned)
            send_message_to_user(submission.user, reply_message)
            review = Review(
                user=user,
                mwe=todays_mwe,
                submission=submission,
                review_type=POSITIVE_REVIEW
            )
            session.add(review)
            session.commit()
            review_handler(user, update, context)
        elif update.message.text == review_types[1]:
            review = Review(
                user=user,
                mwe=todays_mwe,
                submission=submission,
                review_type=NEGATIVE_REVIEW
            )
            session.add(review)
            session.commit()
            review_handler(user, update, context)
        elif update.message.text == review_types[2]:
            review = Review(
                user=user,
                mwe=todays_mwe,
                submission=submission,
                review_type=NEUTRAL_REVIEW
            )
            session.add(review)
            session.commit()
            review_handler(user, update, context)
        elif update.message.text == review_types[3]:
            del context.user_data["submission"]
            del context.user_data["state"]
            update.message.reply_text(
                get_language_token(user.language, Tokens.THANKS_FOR_CONTRIBUTION),
                parse_mode=telegram.ParseMode.MARKDOWN,
                reply_markup=get_main_keyboard_markup(user.language)
            )
    else:
        update.message.reply_text(
            get_language_token(user.language, Tokens.PLEASE_ENTER_VALID_REVIEW),
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=get_review_type_keyboard_keyboard_markup(user.language)
        )


def show_scoreboard_handler(user: User, update: Update, context: CallbackContext):
    user_scores = defaultdict(int)
    points_earned_for_submission = {
        "together": 10,
        "separated": 20,
        "non-mwe": 30
    }

    # user_i: User
    # for user_i in session.query(User).filter(User.language == user.language).all():
    #     submission: Submission
    #     for submission in session.query(Submission).filter(and_(Submission.user_id == user_i.id, Submission.language == user.language)).all():
    #         for review in session.query(Review).filter(and_(Review.submission_id == submission.id, Review.review_type == POSITIVE_REVIEW)).all():
    review: Review
    for review in session.query(Review).all():
        if review.submission.language == user.language and review.review_type == POSITIVE_REVIEW:
            points_earned = points_earned_for_submission[review.submission.category]
            user_scores[review.submission.user] += points_earned

    user_scores_list = list()
    for user_i in user_scores.keys():
        user_scores_list.append([user_i, user_scores[user_i]])

    user_scores_list.sort(key=lambda x: x[1])
    user_scores_list.reverse()

    if len(user_scores_list) > 0:
        scoreboard_message = get_language_token(user.language, Tokens.TOP_FIVE_USERS)
        user_appeared_in_first_five = False
        for i in range(0, 5):
            if i >= len(user_scores_list):
                break
            rankings = ["🥇", "🥈", "🥉", "4.", "5."]
            username = user_scores_list[i][0].username
            if user.id == user_scores_list[i][0].id:
                username = "*%s*" % username
                user_appeared_in_first_five = True
            ranking = rankings[i]
            if user.id == user_scores_list[i][0].id:
                ranking = "*%s*" % ranking
            point = user_scores_list[i][1]
            scoreboard_message += "%s %s - %d" % (ranking, username, point) + "\n"

        if not user_appeared_in_first_five:
            for i in range(len(user_scores_list)):
                if user_scores_list[i][0].id == user.id:
                    scoreboard_message += "...\n"
                    scoreboard_message += "%d. %s - %d" % (i + 1, user.username, user_scores_list[i][1]) + "\n"

        update.message.reply_text(
            scoreboard_message,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard_markup(user.language)
        )
    else:
        update.message.reply_text(
            get_language_token(user.language, Tokens.NO_SUBMISSIONS),
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=get_main_keyboard_markup(user.language)
        )


def message(update: Update, context: CallbackContext):
    try:
        user = get_user_from_update(update)

        if "state" in context.user_data:
            state = context.user_data["state"]
            if state == "changing_language":
                language_update_handler(user, update, context)
            elif state == "submit_example":
                submit_handler_2(user, update, context)
            elif state == "submit_example_type_1":
                submit_handler_3(user, update, context)
            elif state == "submit_example_type_2":
                submit_handler_4(user, update, context)
            elif state == "review":
                review_handler_2(user, update, context)

        else:
            if update.message.text == get_language_token(user.language, Tokens.TODAYS_MWE):
                todays_mwe_handler(user, update, context)
            elif update.message.text == get_language_token(user.language, Tokens.CHANGE_LANGUAGE):
                language_change_handler(user, update, context)
            elif update.message.text == get_language_token(user.language, Tokens.SUBMIT):
                submit_handler(user, update, context)
            elif update.message.text == get_language_token(user.language, Tokens.REVIEW):
                review_handler(user, update, context)
            elif update.message.text == get_language_token(user.language, Tokens.SHOW_SCOREBOARD):
                show_scoreboard_handler(user, update, context)

    except Exception as ex:
        update.message.reply_text(str(ex))


message_handler = MessageHandler(Filters.text, message)
dispatcher.add_handler(message_handler)