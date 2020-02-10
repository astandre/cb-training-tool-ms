from rdflib import Graph, URIRef
from rdflib.namespace import RDF, FOAF
from rdflib import Namespace, Literal

RESOURCE_BASE_URI = "http://127.0.0.1/kbsbot/resources/"
ockb = Namespace("http://127.0.0.1/kbsbot/ontology/")


def build_intents_kg(agent):
    g = Graph()

    agent_uri = URIRef(RESOURCE_BASE_URI + agent.name)

    g.add((agent_uri, RDF.type, ockb.Agent))
    g.add((agent_uri, ockb.agentName, Literal(agent.name)))
    g.add((agent_uri, ockb.agentDescription,
           Literal(agent.about)))

    # telegram_channel_uri = URIRef(RESOURCE_BASE_URI + "OCChatBot")
    #
    # g.add((telegram_channel_uri, RDF.type, ockb.Channel))
    # g.add((telegram_channel_uri, ockb.channelState, Literal("True")))
    # g.add((telegram_channel_uri, ockb.channelAddress, Literal("https://t.me/OCChatBot")))
    # g.add((telegram_channel_uri, ockb.hasSecurityCredentials, Literal("tokendeseguridad")))
    #
    # g.add((agent_uri, ockb.hasChannel, telegram_channel_uri))

    for intent in agent.intents:
        intent_uri = URIRef(RESOURCE_BASE_URI + intent.name)
        print(intent_uri)
        g.add((agent_uri, ockb.hasIntent, intent_uri))
        g.add((intent_uri, RDF.type, ockb.Intent))
        g.add((intent_uri, ockb.intentName, Literal(intent.name)))
        g.add((intent_uri, ockb.intentDescription, Literal(intent.description)))

        answer_uri = URIRef(RESOURCE_BASE_URI + intent.answer.uri)
        print(f"[{answer_uri}]")
        g.add((intent_uri, ockb.hasAnswer, answer_uri))
        g.add((answer_uri, RDF.type, ockb.Answer))
        if intent.answer.answer_template is not None:
            g.add((answer_uri, ockb.answerTemplate, Literal(intent.answer.answer_template)))
        for answ_prop in intent.answer.properties:
            print("[PROPERTY]", answ_prop)
            g.add((answer_uri, ockb.answerProperty, URIRef(answ_prop.name)))
        if intent.answer.refers_to is not None:
            print("[REFERS TO]", intent.answer.refers_to)
            g.add((answer_uri, ockb.refersTo, URIRef(intent.answer.refers_to)))

        if intent.answer.answer_from is not None:
            print("[ANSWER FROM]", intent.answer.answer_from)
            g.add((answer_uri, ockb.answerFrom, URIRef(intent.answer.answer_from)))

        if intent.entities is not None:
            for entity in intent.entities:
                print("[ENTITY]", entity.name)
                g.add((intent_uri, ockb.requiresEntity, URIRef(entity.name)))

        if intent.resolution is not None:
            rq_aux = URIRef(RESOURCE_BASE_URI + intent.resolution.uri)
            print("[RQ]", rq_aux)
            g.add((intent_uri, ockb.hasResolutionQuestion, rq_aux))
            g.add((rq_aux, ockb.hasQuestion, Literal(intent.resolution.question)))
            g.add((rq_aux, ockb.resolves, URIRef(intent.resolution.resolves)))

        for sentence in intent.sentences:
            print(">>>>", sentence)
            g.add((intent_uri, ockb.trainingSentence, Literal(sentence.sentence)))
        # for keyword in intent.keywords:
        #     print(">>>>+++", keyword)
        #     g.add((intent_uri, ockb.intentLabel, Literal(keyword)))

    g.serialize(destination='intents.rdf')
    knowledge = g.serialize(format='json-ld')
    return knowledge
