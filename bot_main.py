import random
from collections import defaultdict

import telegram
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from bot_helpers import get_user_from_update, mwe_category_keyboard_markup, review_type_keyboard_markup, \
    mwe_category_level_1_keyboard_markup, mwe_category_level_2_keyboard_markup, points_earned_for_submission, \
    get_random_congrats_message
from database import session
from submission import Submission
from suggestion import Suggestion
from users import User
import key
from functools import cmp_to_key

updater = Updater(key.TELEGRAM_API_KEY, use_context=True)
dispatcher = updater.dispatcher
bot = dispatcher.bot


def send_message_to_user(user: User, msg: str) -> None:
    bot.send_message(chat_id=user.id,
                     text=msg,
                     parse_mode=telegram.ParseMode.MARKDOWN)


def start(update: Update, context: CallbackContext):
    user = get_user_from_update(update)

    send_message_to_user(user, "Welcome to MWE test, *%s*." % user.username)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def todays_mwe(update: Update, context: CallbackContext):
    update.message.reply_text("Today's MWE is '*give up*', meaning: _cease making an effort; admit defeat._",
                              parse_mode=telegram.ParseMode.MARKDOWN)
    update.message.reply_text("Type */submit* if you want to submit a new example or */review* if you want "
                              "to review an example.",
                              parse_mode=telegram.ParseMode.MARKDOWN)


todays_mwe_handler = CommandHandler('todays_mwe', todays_mwe)
dispatcher.add_handler(todays_mwe_handler)


def submit(update: Update, context: CallbackContext):
    update.message.reply_text("Please enter your example for the MWE: '*to give up*'",
                              parse_mode=telegram.ParseMode.MARKDOWN)
    context.user_data["state"] = "submit_example"


submit_handler = CommandHandler('submit', submit)
dispatcher.add_handler(submit_handler)

def suggest(update: Update, context: CallbackContext):
    update.message.reply_text("Please suggest a new MWE",
                              parse_mode=telegram.ParseMode.MARKDOWN)
    context.user_data["state"] = "suggest_example"

suggest_handler = CommandHandler('suggest', suggest)
dispatcher.add_handler(suggest_handler)

def compare_submissions(s1, s2):
    if s1.users_who_reviewed.count(",") < s2.users_who_reviewed.count(","):
        return -1
    elif s1.users_who_reviewed.count(",") > s2.users_who_reviewed.count(","):
        return 1
    else:
        randnum = random.randint(0, 11)
        if randnum < 3:
            return -1
        elif randnum < 7:
            return 0
        else:
            return 1

def review(update: Update, context: CallbackContext):

    user = get_user_from_update(update)
    all_submissions = session.query(Submission).filter(Submission.user_id != user.id).all()
    all_submissions_for_reviewing = [s for s in all_submissions if str(user.id) not in s.users_who_reviewed]

    if len(all_submissions_for_reviewing) > 0:
        key = cmp_to_key(compare_submissions)
        all_submissions_for_reviewing = sorted(all_submissions_for_reviewing, key=key)
        submission = all_submissions_for_reviewing[0]

        submission_category_messages = {
            "together": 'all the words in “GIVE UP” are 👏 together',
            "separated": 'some words in “GIVE UP” are 🙌 separated',
            "non-mwe": '“GIVE” and “UP” do NOT form a special meaning together ✋ 🤚.'
        }

        reply_message = "'*{}*'. This example was provided for the category where {}."\
            .format(submission.value, submission_category_messages[submission.category])
        update.message.reply_text(reply_message,
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=review_type_keyboard_markup)
        context.user_data["state"] = "review"
        context.user_data['submission'] = submission

    else:
        reply_markup = telegram.ReplyKeyboardRemove()
        update.message.reply_text("Currently there are no examples ready for reviewing. 🙄 Please try later.",
                                  reply_markup=reply_markup)


review_handler = CommandHandler('review', review)
dispatcher.add_handler(review_handler)


def message(update: Update, context: CallbackContext):
    try:
        state = context.user_data["state"]

        if state == "submit_example":
            update.message.reply_text('Does "GIVE UP" form a special meaning in this sentence?',
                                      reply_markup=mwe_category_level_1_keyboard_markup)
            submission = Submission(value=update.message.text)
            context.user_data["submission"] = submission
            context.user_data["state"] = "submit_example_type_1"
        elif state == "submit_example_type_1":
            sub_types = [
                '“GIVE” and “UP” do form a special meaning together 🙌.',
                '“GIVE” and “UP” do NOT form a special meaning together ✋ 🤚.'
            ]
            if update.message.text in sub_types:
                if update.message.text == sub_types[0]:
                    update.message.reply_text('Are the words "GIVE" and "UP" next to each other or are they separated?',
                                              reply_markup=mwe_category_level_2_keyboard_markup)
                    context.user_data["state"] = "submit_example_type_2"
                elif update.message.text == sub_types[1]:
                    user = get_user_from_update(update)
                    submission = context.user_data["submission"]
                    submission.category = "non-mwe"
                    submission.points = 0
                    submission.users_who_reviewed = ''
                    submission.user = user
                    session.add(submission)
                    session.commit()
                    reply_markup = telegram.ReplyKeyboardRemove()
                    update.message.reply_text(get_random_congrats_message() + "! You will win 30 points whenever "
                                                                              "another player likes your example.",
                                              reply_markup=reply_markup)
                    update.message.reply_text("Thank you for your submission. You can now /submit another example "
                                              "or /review other submissions.",
                                              reply_markup=reply_markup)
                    del context.user_data["state"]
                    del context.user_data["submission"]
            else:
                update.message.reply_text("Please choose a valid category.")
            pass
        elif state == "submit_example_type_2":
            sub_types = [
                'All the words in “GIVE UP” are 👏 together',
                'Some words in “GIVE UP” are 🙌 separated'
            ]
            if update.message.text in sub_types:
                user = get_user_from_update(update)
                submission = context.user_data["submission"]
                if update.message.text == 'All the words in “GIVE UP” are 👏 together':
                    submission.category = "together"
                elif update.message.text == 'Some words in “GIVE UP” are 🙌 separated':
                    submission.category = "separated"
                submission.points = 0
                submission.users_who_reviewed = ''
                submission.user = user
                session.add(submission)
                session.commit()
                reply_markup = telegram.ReplyKeyboardRemove()
                if update.message.text == 'All the words in “GIVE UP” are 👏 together':
                    update.message.reply_text("%s! You will win 10 points whenever another player likes "
                                              "your example." % get_random_congrats_message(),
                                              reply_markup=reply_markup)
                elif update.message.text == 'Some words in “GIVE UP” are 🙌 separated':
                    update.message.reply_text("%s! You will win 20 points whenever another player likes "
                                              "your example.." % get_random_congrats_message(),
                                              reply_markup=reply_markup)
                update.message.reply_text("Thank you for your submission. You can now /submit another example "
                                          "or /review other submissions.",
                                          reply_markup=reply_markup)
                del context.user_data["submission"]
                del context.user_data["state"]
            else:
                update.message.reply_text("Please choose a valid category.")
        elif state == 'review':
            review_types = ['👍 I agree. Nice example for this category',
                            '👎 I do not like this example',
                            '⏭ Skip this one',
                            '😱 Quit reviewing']
            user = get_user_from_update(update)
            reply_markup = telegram.ReplyKeyboardRemove()

            if update.message.text in review_types:
                submission = context.user_data["submission"]

                if update.message.text == review_types[0]:
                    print('...user liked')
                    points_earned = points_earned_for_submission[submission.category]
                    submission.points += points_earned
                    reply_message = "%s! Someone else loved your great example, and you’ve earned %d points" \
                                    % (get_random_congrats_message(), points_earned)
                    send_message_to_user(submission.user, reply_message)
                    submission.users_who_reviewed += str(user.id) + ','
                    review(update, context)
                elif update.message.text == review_types[1]:
                    print('...user disliked')
                    submission.users_who_reviewed += str(user.id) + ','
                    review(update, context)
                elif update.message.text == review_types[2]:
                    print('...skipping')
                    review(update, context)
                elif update.message.text == review_types[3]:
                    print('...quitting')
                    update.message.reply_text("Thank you for your contribution!",
                                              reply_markup=reply_markup)
                    del context.user_data["submission"]
                    del context.user_data["state"]
            else:
                update.message.reply_text("Please enter a valid review",
                                          reply_markup=review_type_keyboard_markup)

        elif state == "suggest_example":
            try:
                suggestion = Suggestion(value=update.message.text)
                user = get_user_from_update(update)
                suggestion.category = ""
                suggestion.points = 0
                suggestion.user = user
                session.add(suggestion)
                session.commit()

                update.message.reply_text("Thank you for your contribution!")

                del context.user_data["state"]
            except Exception as ex:
                print(ex)

    except Exception as ex:
        update.message.reply_text(str(ex))


message_handler = MessageHandler(Filters.text, message)
dispatcher.add_handler(message_handler)


def scoreboard(update: Update, context: CallbackContext):
    message_user = get_user_from_update(update)
    user_scores = defaultdict(int)
    for submission in session.query(Submission):
        user_scores[submission.user] += submission.points

    user_scores_list = list()
    for user in user_scores.keys():
        user_scores_list.append([user, user_scores[user]])

    user_scores_list.sort(key=lambda x: x[1])
    user_scores_list.reverse()

    if len(user_scores_list) > 0:
        scoreboard_message = "Here are the top 5 users for today:\n"
        user_appeared_in_first_five = False
        for i in range(0, 5):
            if i >= len(user_scores_list):
                break
            rankings = ["🥇", "🥈", "🥉", "4.", "5."]
            username = user_scores_list[i][0].username
            if message_user.id == user_scores_list[i][0].id:
                username = "*%s*" % username
                user_appeared_in_first_five = True
            ranking = rankings[i]
            if message_user.id == user_scores_list[i][0].id:
                ranking = "*%s*" % ranking
            point = user_scores_list[i][1]
            scoreboard_message += "%s %s - %d" % (ranking, username, point) + "\n"

        if not user_appeared_in_first_five:
            for i in range(len(user_scores_list)):
                if user_scores_list[i][0].id == message_user.id:
                    scoreboard_message += "...\n"
                    scoreboard_message += "%d. %s - %d" % (i + 1, message_user.username, user_scores_list[i][1]) + "\n"
        update.message.reply_text(scoreboard_message,
                                  parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        update.message.reply_text("There are no submissions and users at this time.")




scoreboard_handler = CommandHandler('score', scoreboard)
dispatcher.add_handler(scoreboard_handler)
