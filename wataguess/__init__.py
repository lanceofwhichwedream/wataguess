#!/usr/bin/env python
"""Discord bot built for the purpose of playing WataGuess"""
from discord.ext import commands
from environs import Env
from db import db
from game import game
import logging

__version__ = "0.1.0"


class watabot(object):
    def __init__(self):
        env = Env()
        env.read_env()
        self.data = db(
            {
                "db_user": env("db_user"),
                "db_pass": env("db_pass"),
                "db_host": env("db_host"),
                "db_port": env("db_port"),
            }
        )
        self.logger = self.create_logger()
        self.add_cogs(env("client_token"))

    def create_logger(self):
        logger = logging.getLogger("wataguess")
        logger.setLevel(logging.INFO)
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler("wataguess.log")
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s %(levelname)8s %(message)s")

        c_handler.setFormatter(formatter)
        f_handler.setFormatter(formatter)

        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        return logger

    def add_cogs(self, token):
        description = "Discord Bot for the purpose of playing the Wataguess game!"
        bot = commands.Bot(command_prefix="!", description=description)
        bot.add_cog(game(self.data, self.logger))
        bot.run(token)


if __name__ == "__main__":
    watabot()
