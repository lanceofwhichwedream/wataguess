from pymongo import MongoClient
import logging


class db(object):
    """
    This class connects to the mongo database.
    If the database doesn't exist, pymongo
    will create it.
    """

    def __init__(self, config):
        """
        The constructor for zz8_db_init class.

        Config should be a dict{} containing the
        below variables

        Parameters:
        :param user: The username for db conns
        :type user: str
        :param pass: The password for db conns
        :type pass: str
        :param host: The hostname for db conns
        :type host: str
        :param port: The port for db conns
        :type port: str
        :param db: The port for db conns
        :type db: str
        """
        self.user = config["db_user"]
        self.password = config["db_pass"]
        self.host = config["db_host"]
        self.port = config["db_port"]
        self.logger = logging.getLogger("wataguess")
        self.connection()
        self.dbinit()

    def connection(self):
        """
        Creates the mongo client

        Returns: True
        """
        connect_string = (
            f"mongodb://{self.user}:{self.password}@{self.host}:{self.port}/wataguess",
        )
        try:
            self.client = MongoClient(connect_string)
            self.logger.info("Connected to mongo")
            return True
        except Exception as ex:
            self.logger.error(f"An execption occured\n{ex}")
            return False

    def dbinit(self):
        """
        Sets up the database and creates
        it, if it doesn't already exist

        Returns: True
        """
        self.database = self.client.wataguess
        self.logger.info("Connected to zz8 db")
        return True

    def update_score(self, uuid, score):
        """Upserts uuid and score for that individual

        :param uuid: Universally unique identifier for a user
        :type uuid: INT
        :param score: New score for the user
        :type score: INT
        :return: Returns user's newly updated score
        :rtype: INT
        """
        query = {"uuid": uuid}
        try:
            old_score = self.database.score.find(query)["score"]
            self.logger.info("Retrieved old score for user")
        except Exception as ex:
            self.logger.info(ex)
            old_score = 0
            self.logger.info("No score exists for uuid, brand new player")

        new_score = old_score + score
        dict = {"$set": {"uuid": uuid, "score": new_score}}

        self.database.score.update_one(query, dict, upsert=True)

        return new_score

    def retrieve_score(self, uuid):
        """Retrieves the json for the given user

        :param uuid: Universally unique identifier for a user
        :type uuid: INT
        :return: Returns the stored score for a user
        :rtype: INT
        """
        query = {"uuid": uuid}

        try:
            score = self.database.score.find_one(query)["score"]
        except Exception as ex:
            self.logger.info(ex)
            score = 0
            self.logger.info("Looks like this user has not played yet")

        return score

    def retrieve_top_scores(self):
        """Retrieves the 5 lowest scores (Best performance)

        :return: Mongodb Cursor Object of the 5 lowest scores currently
        :rtype: List
        """
        scores = self.database.score.find().sort("score", -1).limit(5)

        return scores

    def update_item(self, name, price, uid):
        """Upserts item into the database with the name, uid, and price

        :param name: Name of the item to be stored
        :type name: Str
        :param price: Price of the item to be stored
        :type price: Int
        :param uid: Unique ID of the item to be stored
        :type uid: Int
        :return: Since this is focused on getting the item in the database, we return true
        :rtype: True
        """
        query = {"uid": uid}
        item = {"$set": {"uid": uid, "price": price, "name": name}}

        self.database.items.update_one(query, item, upsert=True)
        self.logger.info("Updated item f{uid}")

        return True

    def retrieve_item(self, uid):
        """Retrieves the json for the given item

        :param uid: Universally unique identifier for an item
        :type uid: Int
        :return: Returns either the item as a dict or False
        :rtype: Dict
        """
        query = {"uid": uid}

        try:
            item = self.database.items.find_one(query)
        except Exception as ex:
            self.logger.info(ex)
            item = False
            self.logger.info("Item does not exist currently")

        return item

    def retrieve_recent_item(self):
        """Retrieves the most recently entered item from the database

        :return: Returns the most recent item as a dict
        :rtype: Dict
        """
        recent_item = self.database.items.find().sort("_id", -1).limit(1)[0]

        return recent_item

    def retrieve_all_items(self):
        """Retrieves all items in the database

        :return: Every item as an iterable
        :rtype: List
        """
        all_items = self.database.items.find()

        return all_items
