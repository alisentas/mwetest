from enum import Enum, auto
import random


class Tokens(Enum):
    MAIN_KEYBOARD = auto()
    TODAYS_MWE = auto()
    SUBMIT = auto()
    REVIEW = auto()
    CHANGE_LANGUAGE = auto()
    SUGGEST_MWE = auto()
    SHOW_SCOREBOARD = auto()
    LANGUAGE_ENGLISH = auto()
    LANGUAGE_TURKISH = auto()
    TODAYS_MWE_REPLY_TEXT = auto()
    SELECT_LANGUAGE = auto()
    LANGUAGE_CHANGE_SUCCESSFUL = auto()
    PLEASE_SELECT_VALID_LANGUAGE = auto()
    WELCOME_MESSAGE = auto()
    PLEASE_ENTER_EXAMPLE = auto()
    SPECIAL_MEANING = auto()
    FORM_SPECIAL_MEANING_TOGETHER = auto()
    DOESNT_FORM_SPECIAL_MEANING_TOGETHER = auto()
    ENTER_VALID_MWE_CATEGORY_1 = auto()
    THANKS_FOR_SUBMISSION = auto()
    ARE_WORDS_SEPARATED = auto()
    WORDS_ARE_TOGETHER = auto()
    WORDS_ARE_SEPARATED = auto()
    NO_EXAMPLES_TO_REVIEW = auto()
    AGREE_NICE_EXAMPLE = auto()
    DO_NOT_LIKE_EXAMPLE = auto()
    SKIP_THIS_ONE = auto()
    QUIT_REVIEWING = auto()
    REVIEW_MESSAGE = auto()
    SOMEONE_LOVED_YOUR_EXAMPLE = auto()
    THANKS_FOR_CONTRIBUTION = auto()
    PLEASE_ENTER_VALID_REVIEW = auto()
    TOP_FIVE_USERS = auto()
    NO_SUBMISSIONS = auto()


lang_en = {
    Tokens.TODAYS_MWE: "Today's MWE",
    Tokens.SUBMIT: "Submit",
    Tokens.REVIEW: "Review",
    Tokens.CHANGE_LANGUAGE: "Change language",
    Tokens.SUGGEST_MWE: "Suggest MWE",
    Tokens.SHOW_SCOREBOARD: "Show Scoreboard",
    Tokens.LANGUAGE_ENGLISH: "English (EN)",
    Tokens.LANGUAGE_TURKISH: "Türkçe (TR)",
    Tokens.TODAYS_MWE_REPLY_TEXT: "Today's MWE is '*%s*', meaning: _%s_",
    Tokens.SELECT_LANGUAGE: "Please select a language",
    Tokens.LANGUAGE_CHANGE_SUCCESSFUL: "Language set to *English*.",
    Tokens.PLEASE_SELECT_VALID_LANGUAGE: "Please select a valid language",
    Tokens.WELCOME_MESSAGE: "Welcome to MWExpress, *%s*",
    Tokens.PLEASE_ENTER_EXAMPLE: "Please enter your example for the MWE: '*%s*'",
    Tokens.SPECIAL_MEANING: "Does '%s' form a special meaning in this sentence?",
    Tokens.FORM_SPECIAL_MEANING_TOGETHER: "Words '%s' do form a special meaning together 🙌.",
    Tokens.DOESNT_FORM_SPECIAL_MEANING_TOGETHER: "Words *%s* do NOT form a special meaning together ✋ 🤚.",
    Tokens.ENTER_VALID_MWE_CATEGORY_1: "Please enter a valid category",
    Tokens.THANKS_FOR_SUBMISSION: "%s! Thank you for your submission, you'll win %d points when someone likes your example.",
    Tokens.ARE_WORDS_SEPARATED: 'Are the words "%s" next to each other or are they separated?',
    Tokens.WORDS_ARE_TOGETHER: 'All the words in “%s” are 👏 together',
    Tokens.WORDS_ARE_SEPARATED: 'Some words in “%s” are 🙌 separated',
    Tokens.NO_EXAMPLES_TO_REVIEW: "Currently there are no examples ready for reviewing. 🙄 Please try later.",
    Tokens.AGREE_NICE_EXAMPLE: '👍 I agree. Nice example for this category',
    Tokens.DO_NOT_LIKE_EXAMPLE: '👎 I do not like this example',
    Tokens.SKIP_THIS_ONE: '⏭ Skip this one',
    Tokens.QUIT_REVIEWING: '😱 Quit reviewing',
    Tokens.REVIEW_MESSAGE: "'*%s*'. This example was provided for the category where %s.",
    Tokens.SOMEONE_LOVED_YOUR_EXAMPLE: "%s! Someone else loved your great example, and you’ve earned %d points",
    Tokens.THANKS_FOR_CONTRIBUTION: "Thank you for your contribution!",
    Tokens.PLEASE_ENTER_VALID_REVIEW: "Please enter a valid review",
    Tokens.TOP_FIVE_USERS: "Here are the top 5 users for today:\n",
    Tokens.NO_SUBMISSIONS: "There are no submissions and users at this time."
}

lang_tr = {
    Tokens.TODAYS_MWE: "Bugünün MWEsi",
    Tokens.SUBMIT: "Örnek gönder",
    Tokens.REVIEW: "Örnekleri oyla",
    Tokens.CHANGE_LANGUAGE: "Dili değiştir",
    Tokens.SUGGEST_MWE: "Yeni MWE öner",
    Tokens.SHOW_SCOREBOARD: "Sıralamaları göster",
    Tokens.LANGUAGE_ENGLISH: "English (EN)",
    Tokens.LANGUAGE_TURKISH: "Türkçe (TR)",
    Tokens.TODAYS_MWE_REPLY_TEXT: "Bugünün MWEsi '*%s*', anlamı da: _%s_",
    Tokens.SELECT_LANGUAGE: "Lütfen bir dil seçin",
    Tokens.LANGUAGE_CHANGE_SUCCESSFUL: "Dil *Türkçe* olarak ayarlandı.",
    Tokens.PLEASE_SELECT_VALID_LANGUAGE: "Lütfen geçerli bir dil seçin.",
    Tokens.WELCOME_MESSAGE: "MWExpress'e hoşgeldiniz, *%s*",
    Tokens.PLEASE_ENTER_EXAMPLE: "Lütfen MWE '*%s*' için örneğinizi girin",
    Tokens.SPECIAL_MEANING: "'*%s*' bu cümlede deyimsel bir anlam içeriyor mu?",
    Tokens.FORM_SPECIAL_MEANING_TOGETHER: "'%s' kelimeleri bir arada deyimsel bir anlam ifade ediyor 🙌.",
    Tokens.DOESNT_FORM_SPECIAL_MEANING_TOGETHER: "'%s' kelimeleri bir arada deyimsel bir anlam ifade ETMİYOR ✋ 🤚.",
    Tokens.ENTER_VALID_MWE_CATEGORY_1: "Lütfen geçerli bir kategori seçin",
    Tokens.THANKS_FOR_SUBMISSION: "%s! Gönderiniz için teşekkürler, birisi sizin gönderinizi beğendiğinde %d puan kazanacaksınız.",
    Tokens.ARE_WORDS_SEPARATED: '"%s" kelimeleri örnekte yanyana mı yoksa ayrı mı geçiyor?',
    Tokens.WORDS_ARE_TOGETHER: 'Örnekte “%s” kelimeleri yanyana 👏 geçiyorr',
    Tokens.WORDS_ARE_SEPARATED: 'Örnekte “%s” kelimeleri 🙌 ayrı geçiyor',
    Tokens.NO_EXAMPLES_TO_REVIEW: "Şu an incelebileceğiniz örnek yok. 🙄 Lütfen daha sonra tekrar deneyin.",
    Tokens.AGREE_NICE_EXAMPLE: '👍 Kaıtlıyorum. Bu kategori için güzel bir örnek',
    Tokens.DO_NOT_LIKE_EXAMPLE: '👎 Bu örneği beğenmedim',
    Tokens.SKIP_THIS_ONE: '⏭ Bu örneği geç',
    Tokens.QUIT_REVIEWING: '😱 İncelemeyi bitir',
    Tokens.REVIEW_MESSAGE: "'*%s*'. Bu örnek %s kategorisinde verilmiş.",
    Tokens.SOMEONE_LOVED_YOUR_EXAMPLE: "%s! Birisi örneğini beğendi, sen de %d puan kazandın.",
    Tokens.THANKS_FOR_CONTRIBUTION: "Katkılarınız için teşekkürler!",
    Tokens.PLEASE_ENTER_VALID_REVIEW: "Lütfen geçerli bir inceleme seçin",
    Tokens.TOP_FIVE_USERS: "İşte bugünün ilk beşi:\n",
    Tokens.NO_SUBMISSIONS: "Henüz gönderi ya da oylama yok."
}


def get_language_token(language: str, token: Tokens):
    if language == "en":
        return lang_en[token]
    elif language == "tr":
        return lang_tr[token]
    raise Exception("language %s not found" % language)


congrats_messages = {
    "en": [
        "Nice job",
        "Well done",
        "Super",
        "Awesome",
        "Magnificent",
        "Swell",
        "Superb",
        "Monumental",
        "Fantastic",
        "Grand",
        "Wonderful",
        "Majestic",
        "Stupendous",
        "Spectacular",
        "Colossal",
        "Dynamite",
        "Fabulous",
        "Astounding",
        "Great",
        "Marvelous",
        "Phenomenal",
        "Smashing",
        "Terrific",
        "Tremendous",
        "Prodigious",
        "Cool",
        "Groovy",
        "Extraordinary",
        "Tops",
        "Exemplary",
        "Champion",
        "Superhero"
    ],
    "tr": [
        "Harika",
        "Süper",
        "Yaşasın",
        "Muhteşem"
    ]
}


def get_random_congrats_message(language: str) -> str:
    return congrats_messages[language][random.randint(0, len(congrats_messages[language]) - 1)]