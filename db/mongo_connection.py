from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
    def find_one(
        self, 
        collection_name, 
        query, 
    ):
        """
        查询单条数据
        :param collection_name: 集合名称
        :param query: 查询条件 (e.g. {"username": "john"})
        :param projection: 返回字段过滤 (e.g. {"_id": 0, "name": 1})
        :return: 文档字典或None
        """
        return self.db[collection_name].find_one(query)

    def insert_data(
        self, 
        collection_name, 
        data
    ):
        """
        插入单条数据
        :param collection_name: 集合名称
        :param data: 要插入的文档字典
        :return: 插入文档的_id (str格式)
        """
        result = self.db[collection_name].insert_one(data)
        return result.inserted_id