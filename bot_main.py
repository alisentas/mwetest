import random

import telegram
from telegram import Update, ChatAction
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from bot_helpers import get_user_from_update, mwe_category_keyboard_markup, review_type_keyboard_markup
from database import session
from submission import Submission
from users import User
import key

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
    update.message.reply_text("Today's MWE is '*to give up*', meaning: _cease making an effort; admit defeat._",
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


def review(update: Update, context: CallbackContext):
    all_submissions = session.query(Submission).all()
    if len(all_submissions) > 0:
        submission = all_submissions[random.randrange(0, len(all_submissions))]
        update.message.reply_text("Please enter your review for: '*" + submission.value + "*'. This is described as '*"
                                  + submission.category + "*'",
                                  parse_mode=telegram.ParseMode.MARKDOWN,
                                  reply_markup=review_type_keyboard_markup)
        context.user_data["state"] = "review"
        context.user_data['submission'] = submission
    else:
        update.message.reply_text("There are no examples right now, be the first one to /submit.")


review_handler = CommandHandler('review', review)
dispatcher.add_handler(review_handler)


def message(update: Update, context: CallbackContext):
    try:
        state = context.user_data["state"]

        if state == "submit_example":
            update.message.reply_text("Now please choose category of this example.",
                                      reply_markup=mwe_category_keyboard_markup)
            submission = Submission(value=update.message.text)
            context.user_data["submission"] = submission
            context.user_data["state"] = "submit_example_type"
        elif state == "submit_example_type":
            sub_types = ['contiguous instance for usage as a MWE',
                         'non-contiguous instance for usage as a MWE',
                         'instance for usage as non-MWE',
                         'synonym substitution for an instance',
                         'antonym substitution for an instance',
                         'other']
            if update.message.text in sub_types:
                user = get_user_from_update(update)
                submission = context.user_data["submission"]
                submission.category = update.message.text
                submission.points = 0
                submission.user = user
                session.add(submission)
                session.commit()
                reply_markup = telegram.ReplyKeyboardRemove()
                update.message.reply_text("Thank you for your submission, you can now /submit another example "
                                          "or /review other submissions.",
                                          reply_markup=reply_markup)
                del context.user_data["submission"]
                del context.user_data["state"]
            else:
                update.message.reply_text("Please enter a valid MWE category",
                                          reply_markup=mwe_category_keyboard_markup)
        elif state == 'review':
            review_types = ['good',
                            'bad',
                            "don't know"]
            if update.message.text in review_types:
                submission = context.user_data["submission"]
                if update.message.text == 'good':
                    submission.points += 1
                    send_message_to_user(submission.user, "Someone liked your example '*"
                                         + submission.value + "*', nice job.")
                elif update.message.text == 'bad':
                    submission.points -= 1
                    send_message_to_user(submission.user, "Someone disliked your example '*"
                                         + submission.value + "*', better luck next time.")
                session.commit()
                reply_markup = telegram.ReplyKeyboardRemove()
                update.message.reply_text("Thank you for your review, you can now /submit another example "
                                          "or /review other submissions.",
                                          reply_markup=reply_markup)
                del context.user_data["submission"]
                del context.user_data["state"]
            else:
                update.message.reply_text("Please enter a valid review",
                                          reply_markup=review_type_keyboard_markup)

    except KeyError:
        update.message.reply_text('Not found')


message_handler = MessageHandler(Filters.text, message)
dispatcher.add_handler(message_handler)