import pymongo

class Dataset(object):
    def __init__(self, **kwargs):
        if 'host' not in kwargs:
            raise TypeError('host must be provide')

        if 'port' not in kwargs:
            raise TypeError('port must be provide')
        
        if 'username' not in kwargs:
            raise TypeError('username must be provide')

        if 'password' not in kwargs:
            raise TypeError('host must be provide')
        
        if 'database' not in kwargs:
            raise TypeError('database must be provide')
        
        self.client = pymongo.MongoClient(host=kwargs['host'], 
                  port=kwargs['port'], username=kwargs['username'], password=kwargs['password'], authMechanism='SCRAM-SHA-256')
        
        self.db = self.client[kwargs['database']]

        self.dataset_collection = self.db['dataset']
        x = self.dataset_collection.delete_one({})
        x.deleted_count
    
    def insert_one(self, data = {}):
      inserted = self.dataset_collection.insert_one(data)
      return inserted.inserted_id

    def insert_documents(self, data = []):
      inserted = self.dataset_collection.insert_many(data)
      return inserted.inserted_ids
    
    def update_one(self, tag, new_data = {}):
      updated = self.dataset_collection.update_one({'tag': tag}, new_data)
      return updated.modified_count

    def delete(self, tag):
      deleted = self.dataset_collection.delete_one({'tag': tag})
      return deleted.deleted_count

    def find_by_tag(self, tag):
      return self.dataset_collection.find_one({'tag': tag})
    
    def find_all(self):
      datas = []
      for d in self.dataset_collection.find():
        datas.append(d)
      return datas

    def close(self):
      self.client.close()
  

# host = 'localhost'
# port = 27017
# username = 'bot'
# password = 'bot'
# database = 'bot_dataset'

# data = {
#         "tag": "selamattinggal",
#         "patterns": [
#           "Dah",
#           "Sampai jumpa lagi",
#           "Dadah",
#           "bye",
#           "Selamat tinggal"
#         ],
#         "responses": [
#           "Sampai jumpa lagi, terima kasih sudah berkunjung",
#           "Semoga harimu menyenangkan",
#           "Dadah, silahkan kembali lagi secepatnya"
#         ]
#       }

# datastore = Dataset(host=host, port=port, username=username, password=password, database=database)

# data = datastore.find_all()
# print(data[:4])

# datastore.close()