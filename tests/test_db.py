import pytest
from pytest_mongodb.plugin import mongomock
from pytest_mongodb.plugin import pymongo
from wataguess.db import db


config = {
    "db_user": "test",
    "db_pass": "test",
    "db_host": "127.0.0.1",
    "db_port": 27017,
}


class Testdb:
    @pytest.fixture
    def db(self):
        watadb = db(config)
        return watadb

    def test_init(self, db):
        assert db.user == config["db_user"]
        assert db.password == config["db_pass"]
        assert db.host == config["db_host"]
        assert db.port == config["db_port"]
        assert isinstance(db.client, pymongo.mongo_client.MongoClient)
        assert isinstance(db.db, pymongo.database.Database)

    def test_connection(self, db):
        db.connection()
        assert isinstance(db.client, pymongo.mongo_client.MongoClient)

    def test_dbinit(self, db):
        db.dbinit()
        assert isinstance(db.db, pymongo.database.Database)

    def test_collection_presence(self, mongodb):
        assert "items" in mongodb.list_collection_names()
        assert "score" in mongodb.list_collection_names()

    def test_score_update(self, db, mongodb):
        db.db = mongodb
        user = 989767856876
        score = 500
        user1 = db.update_score(user, score)
        query = {"uuid": user}
        assert user1 == 500
        test_user = mongodb.score.find_one(query)
        assert test_user["score"] == score
        assert test_user["uuid"] == user

    def test_score_retrieval(self, db, mongodb):
        db.db = mongodb
        user1 = 7342754
        user2 = 93452345
        user3 = 832435632456
        user4 = 3246584567

        score1 = db.retrieve_score(user1)
        score2 = db.retrieve_score(user2)
        score3 = db.retrieve_score(user3)
        score4 = db.retrieve_score(user4)

        assert isinstance(score1, int)
        assert isinstance(score2, int)
        assert isinstance(score3, int)
        assert isinstance(score4, int)

        assert score1 == 500
        assert score2 == 420
        assert score3 == 999999
        assert score4 == 0

        query1 = {"uuid": user1}
        query2 = {"uuid": user2}
        query3 = {"uuid": user3}

        assert score1 == mongodb.score.find_one(query1)["score"]
        assert score2 == mongodb.score.find_one(query2)["score"]
        assert score3 == mongodb.score.find_one(query3)["score"]

    def test_item_update(self, db, mongodb):
        db.db = mongodb
        item1 = {"name": "this is a name", "price": 55.50, "uid": 542345}
        item2 = {"name": "pokemon box ruby sapphire", "price": 2000, "uid": 2354323}
        item3 = {"name": "mario", "price": 1000000, "uid": 9587643}

        assert db.update_item(item1["name"], item1["price"], item1["uid"])
        assert db.update_item(item2["name"], item2["price"], item2["uid"])
        assert db.update_item(item3["name"], item3["price"], item3["uid"])

        query1 = {"uid": item1["uid"]}
        query2 = {"uid": item2["uid"]}
        query3 = {"uid": item3["uid"]}

        test_item1 = mongodb.items.find_one(query1)
        test_item2 = mongodb.items.find_one(query2)
        test_item3 = mongodb.items.find_one(query3)

        assert item1.items() <= test_item1.items()
        assert item2.items() <= test_item2.items()
        assert item3.items() <= test_item3.items()

    def test_item_retrival(self, db, mongodb):
        db.db = mongodb
        item1 = 231341245
        item2 = 4598623457
        item3 = 354265423546

        test_item1 = db.retrieve_item(item1)
        test_item2 = db.retrieve_item(item2)
        test_item3 = db.retrieve_item(item3)

        assert isinstance(test_item1, dict)
        assert isinstance(test_item2, dict)
        assert test_item3 == None

        assert test_item1["uid"] == item1
        assert test_item1["price"] == 420.69
        assert test_item1["name"] == "pokemon box"
        assert test_item2["uid"] == item2
        assert test_item2["price"] == 65
        assert test_item2["name"] == "ska vinyl"

        query1 = {"uid": item1}
        query2 = {"uid": item2}

        assert test_item1.items() <= mongodb.items.find_one(query1).items()
        assert test_item2.items() <= mongodb.items.find_one(query2).items()

    def test_recent_item_retrival(self, db, mongodb):
        db.db = mongodb

        test_item1 = db.retrieve_recent_item()

        assert (
            test_item1.items()
            <= mongodb.items.find().sort("_id", -1).limit(1)[0].items()
        )

        item2 = {"name": "this is a name", "price": 55.50, "uid": 542345}

        assert db.update_item(item2["name"], item2["price"], item2["uid"])

        query2 = {"uid": item2["uid"]}

        assert mongodb.items.find_one(query2)

        test_item2 = db.retrieve_recent_item()

        assert item2.items() <= test_item2.items()

    def test_every_item_retrival(self, db, mongodb):
        db.db = mongodb

        items = mongodb.items.find()

        all_items = db.retrieve_all_items()

        for i in [0, 1]:
            assert items[i].items() <= all_items[i].items()

    def test_retrieve_top_scores(self, db, mongodb):
        db.db = mongodb

        users = mongodb.score.find().sort("score", -1).limit(5)

        top_users = db.retrieve_top_scores()

        for i in [0, 1, 2]:
            assert users[i].items() <= top_users[i].items()
