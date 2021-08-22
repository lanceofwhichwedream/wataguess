import asyncio
import discord
import discord.ext.test as dpytest
import pytest
import logging
import requests_mock

# from wataguess.game import Game
from discord.ext import commands, tasks
from wataguess import watabot, game

logger = logging.getLogger("wataguess")


class TestWataguess(object):
    #    @pytest.fixture
    #    def bot(self, event_loop, monkeypatch):
    #        monkeypatch.setenv("db_user", "test")
    #        monkeypatch.setenv("db_pass", "test")
    #        monkeypatch.setenv("db_host", "127.0.0.1")
    #        monkeypatch.setenv("db_port", "27017")
    #        monkeypatch.setenv("client_token", "123414351345")
    #        bot = watabot()
    #
    #        return bot
    #
    #    def test_bot_config(self, bot):
    #        assert bot.data.user == "test"
    #        assert bot.data.password == "test"
    #        assert bot.data.host == "127.0.0.1"
    #        assert bot.data.port == 27017
    #

    @pytest.fixture
    def bot(self, event_loop, monkeypatch):
        monkeypatch.setenv("db_user", "test")
        monkeypatch.setenv("db_pass", "test")
        monkeypatch.setenv("db_host", "127.0.0.1")
        monkeypatch.setenv("db_port", "27017")
        monkeypatch.setenv("client_token", "123414351345")
        intents = discord.Intents.default()
        intents.members = True
        bot = commands.Bot(command_prefix="!", loop=event_loop, intents=intents)
        bot.add_cog(game.Game(bot, logger))

        return bot

    @pytest.mark.asyncio
    @requests_mock.Mocker(kw="m")
    async def test_wataguess_start(self, bot, **kwargs):
        dpytest.configure(bot)
        guild = dpytest.get_config().guilds[0]
        dpytest.backend.make_member(
            dpytest.backend.make_user("lance", "0001"),
            guild,
            roles=[dpytest.backend.make_role("user", guild, permissions=8)],
        )
        url = "https://www.ebay.com/itm/224566589033?_trkparms=aid%3D111001%26algo%3DREC.SEED%26ao%3D1%26asc%3D20160908105057%26meid%3D3f3b891cdc0a4ec897738b58da9bfb9a%26pid%3D100675%26rk%3D3%26rkt%3D15%26sd%3D234134140352%26itm%3D224566589033%26pmt%3D0%26noa%3D1%26pg%3D2380057&_trksid=p2380057.c100675.m4236&_trkparms=pageci%3Af400876c-fca9-11eb-88f8-465ff8f2a923%7Cparentrq%3A428e8d7917b0a64d565ad810ffe02b58%7Ciid%3A1"
        item = "mario"
        kwargs["m"].get(
            "https://www.ebay.com/itm/224566589033?_trkparms=aid%3D111001%26algo%3DREC.SEED%26ao%3D1%26asc%3D20160908105057%26meid%3D3f3b891cdc0a4ec897738b58da9bfb9a%26pid%3D100675%26rk%3D3%26rkt%3D15%26sd%3D234134140352%26itm%3D224566589033%26pmt%3D0%26noa%3D1%26pg%3D2380057&_trksid=p2380057.c100675.m4236&_trkparms=pageci%3Af400876c-fca9-11eb-88f8-465ff8f2a923%7Cparentrq%3A428e8d7917b0a64d565ad810ffe02b58%7Ciid%3A1",
            text='<span class="notranslate", id="prcIsum_bidPrice" itemprop="price" content="420.60">US $420.69</span><meta Property="og:title" Content="mario" />',
        )
        await dpytest.message(f"!wataguess {url}")
        assert dpytest.verify().message().content("Got it! Give me one moment...")
        await asyncio.sleep(20)
        assert dpytest.verify().message().content("Come one! Come all!")
        await asyncio.sleep(1)
        assert (
            dpytest.verify().message().content("Time for the next round of WataGuess!")
        )
        await asyncio.sleep(3)
        assert dpytest.verify().message().content(f"The new item is {item}")
        await asyncio.sleep(3)
        assert dpytest.verify().message().content("Good luck and have fun!")
