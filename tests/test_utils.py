from wataguess import utils
import pytest
import requests_mock


def test_one():
    test_url = "https://www.ebay.com/itm/224566589033?_trkparms=aid%3D111001%26algo%3DREC.SEED%26ao%3D1%26asc%3D20160908105057%26meid%3D3f3b891cdc0a4ec897738b58da9bfb9a%26pid%3D100675%26rk%3D3%26rkt%3D15%26sd%3D234134140352%26itm%3D224566589033%26pmt%3D0%26noa%3D1%26pg%3D2380057&_trksid=p2380057.c100675.m4236&_trkparms=pageci%3Af400876c-fca9-11eb-88f8-465ff8f2a923%7Cparentrq%3A428e8d7917b0a64d565ad810ffe02b58%7Ciid%3A1"
    clean_url = utils.clean_url(test_url)
    assert clean_url == "https://www.ebay.com/itm/224566589033"


@requests_mock.Mocker(kw="m")
def test_two(**kwargs):
    test_url = "http://blarg.comitm/143251345"
    kwargs["m"].get(
        "http://blarg.comitm/143251345",
        text='<span class="notranslate" id="prcIsum_bidPrice" itemprop="price" content="420.60">US $420.69</span><meta Property="og:title" Content="Pokemon Box: Ruby and Sapphire (GameCube) NTSC US Disc w/ Case, Manual, Stickers 45496961442 | eBay" />',
    )
    item, price, item_id = utils.get_data(test_url)
    assert (
        item
        == "Pokemon Box: Ruby and Sapphire (GameCube) NTSC US Disc w/ Case, Manual, Stickers 45496961442 | eBay"
    )
    assert price == "420.69"
    assert item_id == "143251345"
