from flakon import JsonBlueprint
from flask import request
from kbsbot.training_tool.mongo import *
from kbsbot.training_tool.kg import *
from kbsbot.training_tool.database import *
import logging

train = JsonBlueprint('train', __name__)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


@train.route('/interactions/all', methods=["GET"])
def all_threads():
    """
    This view returns a list of all  interactions of an agent .

    Args:
        @param: agent: This view requires an agent name.

    """
    logger.info(">>>>> Incoming data  %s", request.args)
    if "agent" in request.args:
        agent = request.args.get('agent')
        agent = Agent.query.filter_by(name=agent).first()
        if agent is not None:
            result = get_interactions(agent.name)
            # TODO get 10 sentences
            output = {
                "interactions": result
            }
        else:
            output = {"message": "Must provide a valid agent name"}
    else:
        output = {"message": "Must provide a valid agent name"}

    logger.info("<<<<< Output  %s", output)
    return output


@train.route('/kg', methods=["GET"])
def make_kg():
    data = request.get_json()
    logger.info(">>>>> Incoming data  %s", data)
    if "agent" in data:
        agent = Agent.query.filter_by(name=data["agent"]).first()
        knowledge = build_intents_kg(agent)

        output = {"agent": agent.name, "knowledge": str(knowledge)}
    else:
        output = {"message": "Must provide a valid agent"}
    logger.info("<<<<< Output  %s", output)
    return output


@train.route('/kg/new/sentence', methods=["POST"])
def new_sentence():
    data = request.get_json()
    logger.info(">>>>> Incoming data  %s", data)
    if "agent" in data and "sentence" in data and "intent" in data:
        if "mongo_id" in data:
            sentence, intent = new_classified_sentence(data["agent"], data["intent"], data["sentence"],
                                                       data["mongo_id"])
            update_entry(data["mongo_id"])
        else:
            sentence, intent = new_classified_sentence(data["agent"], data["intent"], data["sentence"])
        output = {"sentence": sentence, "intent": intent}
    else:
        output = {"message": "Not valid data."}
    logger.info("<<<<< Output  %s", output)
    return output


@train.route('/kg/intents', methods=["GET"])
def get_intents_agent():
    logger.info(">>>>> Incoming data  %s", request.args)
    if "agent" in request.args:
        agent = request.args.get('agent')
        agent = Agent.query.filter_by(name=agent).first()
        if agent is not None:
            intents = []
            for intent in agent.intents:
                if intent.proposed is False:
                    intents.append(
                        {"name": intent.name, "description": intent.description,
                         "proposed": intent.proposed})
            output = {"agent": agent.name, "intents": intents}
        else:
            output = {"message": "Not valid data."}
    else:
        output = {"message": "Not valid data."}
    logger.info("<<<<< Output  %s", output)
    return output


@train.route('/kg/sentences', methods=["GET"])
def get_sentence_intent():
    logger.info(">>>>> Incoming data  %s", request.args)
    if "intent" in request.args:
        intent = request.args.get('intent')
        intent = Intent.query.filter_by(name=intent).first()
        if intent is not None:
            sentences = []
            for sentence in intent.sentences:
                sentences.append(sentence.sentence)
            output = {"intent": intent.name, "sentences": sentences}
        else:
            output = {"message": "Not valid data."}
    else:
        output = {"message": "Not valid data."}
    logger.info("<<<<< Output  %s", output)
    return output
