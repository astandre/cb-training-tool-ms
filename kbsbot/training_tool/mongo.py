from pymongo import MongoClient
from pymongo import DESCENDING
from bson.objectid import ObjectId
import os

MONGO_HOST = os.environ.get('MONGO_HOST')
client = MongoClient(MONGO_HOST)

# client = MongoClient("mongodb://localhost:27017/")
db = client["interactions_db"]
interactions = db["interactions"]


def update_entry(entry_id):
    """
    This method updates the classified status of an interaction

     Parameters:

        :param entry_id: The id of the message.

    """

    # "context": {"classified": False}
    updated_entry = interactions.find_one({'_id': ObjectId(entry_id)})
    print(updated_entry["output"]["context"])
    aux_output = updated_entry["output"]
    output = aux_output["context"]["classified"] = True
    interactions.update({'_id': ObjectId(entry_id)}, {'$set': {"output": output}})


def get_interactions(agent):
    """
    This method retrieves all of unclassified user-agent interactions

    :param agent: A valid agent name.

    :return: a list of all interactions
    """
    result = interactions.find({"agent": agent, "output.context.classified": False},
                               sort=[('date', DESCENDING)])
    final_res = []
    for res in result:
        aux_res = {
            "id": str(res["_id"]),
            "agent": res["agent"],
            "sentence": res["input"]["user_input"]
        }
        final_res.append(aux_res)
    return final_res
