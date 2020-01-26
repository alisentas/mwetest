from users import User
from database import session
from bot_main import updater
from flask import Flask, escape, request

updater.start_polling()
updater.idle()