from cachetools import cached
from flask import Flask


@cached({})
def get_app():
    adv = Flask("app")

    return adv
