from pymongo import MongoClient
from bson.objectid import ObjectId
import os

MONGO_HOST = os.environ.get('MONGO_HOST')
client = MongoClient(MONGO_HOST)

# client = MongoClient("mongodb://localhost:27017/")
db = client["interactions_db"]
interactions = db["interactions"]


def get_all_inputs():
    inter = interactions.find()
    # print(inter)
    for aux in inter:
        print(aux)


def update_entry(entry_id):
    """
    This method updates the output of the current conversation thread.

     Parameters:

        :param entry_id: The id of the message.

    """

    # "context": {"classified": False}
    updated_entry = interactions.update({'_id': ObjectId(entry_id)})
    print(updated_entry["output"]["context"])
    context = updated_entry["output"]["context"]["classified"] = True
    interactions.update({'_id': ObjectId(entry_id)}, {'$set': {"output": context}})


def get_interactions(agent):
    result = interactions.find({"agent": agent, "context": {"classified": False}})
    final_res = []
    # TODO get 10 sentences
    print(len(result))
    for res in result:
        # print(res)
        aux_res = {
            "id": str(res["_id"]),
            "agent": res["agent"],
            "sentence": res["input"]["user_input"]
        }
        final_res.append(aux_res)
    return final_res

# print(get_interactions("OpenCampus"))
# get_all_inputs()
