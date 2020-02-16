from kbsbot.training_tool.app import create_app
from kbsbot.training_tool.database import *
from kbsbot.training_tool.kg import *
from unittest import TestCase
import json


class TestAPP(TestCase):

    # this method is run before each test
    def setUp(self):
        app = create_app()
        self.client = app.test_client()
        db.init_app(app)
        db.app = app
        db.create_all(app=app)
        self.agent = Agent(name='OpenCampus',
                           about="Este es el chabot de Open Campus capaz de resolver dudas sobre los diferentes cursos de la oferta actual de Open Campus")
        description_prop = Property(name="http://127.0.0.1/ockb/course/ontology/description")

        ObtenerInformacionAnswer = Answer(uri="ObtenerInformacionAnswer", answer_template="{%description%}",
                                          properties=[description_prop])

        curso_entity = Entity(name="http://127.0.0.1/ockb/course/resource/Course")

        # setting up synonyms:
        Synonym(name="Mooc", entity=curso_entity)

        # Setting up resolution
        ObtenerInformacionResolution = Resolution(uri="ObtenerInformacionResolution",
                                                  question="De que cursos deseas conocer",
                                                  resolves="http://127.0.0.1/ockb/course/resource/Course")

        ObtenerInformacion = Intent(name="ObtenerInformacion", agent=self.agent,
                                    description="Obtener una breve descripcion del curso",
                                    answer=ObtenerInformacionAnswer, resolution=ObtenerInformacionResolution,
                                    entities=[curso_entity])

        Sentence(intent=ObtenerInformacion, sentence="De que trata el mooc?")
        Sentence(intent=ObtenerInformacion, sentence="Quiero informacion del curso de emprendimiento")
        Sentence(intent=ObtenerInformacion, sentence="Muestrame un resumen del mooc?")
        Sentence(intent=ObtenerInformacion, sentence="Breve introducción al curso")
        Sentence(intent=ObtenerInformacion, sentence="que es emprendimiento")
        Sentence(intent=ObtenerInformacion, sentence="De que se trata el curso?")
        Sentence(intent=ObtenerInformacion, sentence="De qué va el curso?")
        Sentence(intent=ObtenerInformacion, sentence="Me ayudas con información acerca del curso?")

        db.session.add(self.agent)
        db.session.commit()

    # this method is run after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_intents_agent(self):
        response = self.client.get(
            '/kg/intents', query_string={'agent': 'OpenCampus'},
        )
        self.assertEqual(response.status_code, 200)
        data_resp = json.loads(response.data.decode('utf-8'))
        self.assertIn("agent", data_resp)
        self.assertIn("intents", data_resp)
        self.assertTrue(len(data_resp["intents"]) > 0)

        response = self.client.get(
            '/kg/intents', query_string={'agent': 'ComidadeQueso'},
        )
        self.assertEqual(response.status_code, 200)
        data_resp = json.loads(response.data.decode('utf-8'))
        self.assertIn("message", data_resp)

    def test_get_sentence_intent(self):
        response = self.client.get(
            '/kg/sentences', query_string={'intent': 'ObtenerInformacion'},
        )
        self.assertEqual(response.status_code, 200)
        data_resp = json.loads(response.data.decode('utf-8'))
        self.assertIn("intent", data_resp)
        self.assertIn("sentences", data_resp)
        self.assertTrue(len(data_resp["sentences"]) > 0)

        response = self.client.get(
            '/kg/intents', query_string={'intent': 'ComerQueso'},
        )
        self.assertEqual(response.status_code, 200)
        data_resp = json.loads(response.data.decode('utf-8'))
        self.assertIn("message", data_resp)

    def test_new_sentence(self):
        data = dict(
            sentence="De que se trata el curso emprendimiento",
            intent="ObtenerInformacion",
            agent="OpenCampus"

        )
        response = self.client.post(
            '/kg/new/sentence', data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data_resp = json.loads(response.data.decode('utf-8'))
        self.assertIn("intent", data_resp)
        self.assertIn("sentence", data_resp)
        self.assertTrue(data_resp["sentence"] == data["sentence"])
        self.assertTrue(data_resp["intent"] == data["intent"])

    def test_build_intents_kg(self):
        result = build_intents_kg(self.agent)
        self.assertTrue(len(result) > 0)

    def test_make_uri(self):
        result = make_uri("asdad asd ads a 99 88 22 !@#$%^&*()/*-+ 123456 ")
        characters = [" !@#$%^&*()/*-+123456789"]
        for aux_char in characters:
            self.assertTrue(aux_char not in result)
