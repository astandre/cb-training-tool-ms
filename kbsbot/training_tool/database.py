from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

RESOURCE_BASE_URI = "http://127.0.0.1/kbsbot/resources/"


class Agent(db.Model):
    """Agent

    An Agent refers to the main o domain or purpose of the chatbot.

    Attributes:
        :param @id: Id to populate the database.

        :param @name: This name must be unique to identify the Agent.

        :param @about: A description of the purpose of the chatbot.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    about = db.Column(db.String(140), nullable=False)

    def __repr__(self):
        return f"<Agent {self.name}>"


entities = db.Table('entities',
                    db.Column('intent_id', db.Integer, db.ForeignKey('intent.id'), primary_key=True),
                    db.Column('entity_id', db.Integer, db.ForeignKey('entity.id'), primary_key=True)
                    )


class Entity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True)

    def __repr__(self):
        return f"<Entity {self.name}>"


class Synonym(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True)
    entity_id = db.Column(db.Integer, db.ForeignKey('entity.id'), nullable=False)
    entity = db.relationship('Entity', backref=db.backref('synonyms', lazy=True))

    def __repr__(self):
        return f"<Synonym {self.name}>"


class Keyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True)
    intent_id = db.Column(db.Integer, db.ForeignKey('intent.id'), nullable=False)
    intent = db.relationship('Intent', backref=db.backref('keywords', lazy=True))

    def __repr__(self):
        return f"<Agent {self.name}>"


class Intent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(140), nullable=False)
    # Relationships one to one for answer
    answer_id = db.Column(db.Integer, db.ForeignKey('answer.id'))
    answer = db.relationship('Answer', backref='intent')
    # Relationships one to one for resolution question
    resolution_id = db.Column(db.Integer, db.ForeignKey('resolution.id'))
    resolution = db.relationship('Resolution', backref='intent')
    # Relationships many to one for agent.
    agent_id = db.Column(db.Integer, db.ForeignKey('agent.id'), nullable=False)
    agent = db.relationship('Agent', backref=db.backref('intents', lazy=True))
    # Relationships for entities
    entities = db.relationship('Entity', secondary=entities, lazy='subquery',
                               backref=db.backref('intents', lazy=True))

    def __repr__(self):
        return f"<Intent {self.name}>"


class Sentence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mongo_id = db.Column(db.String(20), nullable=True)
    sentence = db.Column(db.String(300), nullable=False)
    intent_id = db.Column(db.Integer, db.ForeignKey('intent.id'), nullable=False)
    intent = db.relationship('Intent', backref=db.backref('sentences', lazy=True))

    def __repr__(self):
        return f"<Sentence {self.sentence}>"


properties = db.Table('properties',
                      db.Column('answer_id', db.Integer, db.ForeignKey('answer.id'), primary_key=True),
                      db.Column('property_id', db.Integer, db.ForeignKey('property.id'), primary_key=True)
                      )


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(300), unique=True, nullable=False)
    answer_template = db.Column(db.String(300), nullable=False)
    properties = db.relationship('Property', secondary=properties, lazy='subquery',
                                 backref=db.backref('answers', lazy=True))

    refers_to = db.Column(db.String(300), nullable=True)
    answer_from = db.Column(db.String(300), nullable=True)

    def __str__(self):
        return f"<Answer {RESOURCE_BASE_URI}{self.uri}>"


class Property(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)

    def __str__(self):
        return f"<Property {self.name}>"


class Resolution(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uri = db.Column(db.String(300), nullable=False)
    question = db.Column(db.String(300), nullable=False)
    resolves = db.Column(db.String(300), nullable=False)

    def __str__(self):
        return f"<Answer {RESOURCE_BASE_URI}{self.uri}>"


def get_agent(agent_name):
    """
    This methods finds the agent object by filtering by its name

     Parameters:
        :param agent_name: The name of the agent.

      Return:
        The agent object object if found.
    """
    current_agent = Agent.query.filter_by(name=agent_name).first()
    if current_agent is not None:
        return current_agent


def new_classified_sentence(agent_name, intent, sentence, mongo_id=None):
    """
    Add new classified sentence

     Parameters:
        :param agent_name: The name of the agent.

        :param intent: The name of and Intent.

        :param sentence: A new sentence.

        :param mongo_id: Id of the interaction.

      Return:
        The sentence if added.
    """
    agent = Agent.query.filter_by(name=agent_name).first()
    selected_intent = Intent.query.filter_by(agent=agent, name=intent).first()
    if mongo_id is not None:
        db.session.add(Sentence(intent=selected_intent, sentence=sentence))
    else:
        db.session.add(Sentence(intent=selected_intent, sentence=sentence, mongo_id=mongo_id))
    db.session.commit()
    return sentence
