import time

from pymongo import MongoClient, UpdateOne, UpdateMany

# Connect to the MongoDB instance and switch to the relevant database

client = MongoClient('mongodb://usndtaxtdacdb09:cfXF4GWmQyyabx2BUeOa7yVswC5tfXpMhltfQPgGFCaJQru15dIV3E8A5QaDfquRx6Awz7wO7LHrACDbUwFMfg%3D%3D@usndtaxtdacdb09.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@usndtaxtdacdb09@')

db = client['TADADB']

collection = db['UnclassifiedTxs']

# Use find() to create a cursor to iterate over the documents

# cursor = collection.find()

batch_size = 1000 # Update documents in batches of 1000

# Use a loop to iterate over the documents and update them

count = 0

requests =[]

# for doc in cursor:

#     requests.append(UpdateOne({'isdelete': {"$exists": False}}, {'$set': {'isdelete': False}}))

#     count += 1

update_query = {'$set': {'isdelete': False}}

for doc in collection.find({"Wallet":{"$exists":True}}):

    # requests.append(UpdateMany({'isdelete': {"$exists": False}}, {'$set': {'isdelete': False}}))

    requests.append(UpdateOne( { '_id': doc['_id'] }, update_query ))

    count += 1

    # Write the updated documents in batches

    # if count % batch_size == 0:

    if len(requests) == batch_size:

        # time.sleep(2)

        # collection.bulk_write(requests, ordered=False)

        collection.bulk_write(requests)

        requests = []
# Write the remaining documents

if requests:

    # collection.bulk_write(requests, ordered=False)

    collection.bulk_write(requests)




print(f'{count} documents updated.')
