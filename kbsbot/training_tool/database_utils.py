from kbsbot.training_tool.database import *


def init_database():
    """
    This function is used to initially populate the database
    """
    exists = Agent.query.all()
    if exists is None or len(exists) == 0:
        # Setting up agent
        agent = Agent(name='OpenCampus',
                      about="Este es el chabot de Open Campus capaz de resolver dudas sobre los diferentes cursos de la oferta actual de Open Campus")

        db.session.add(agent)

        # Setting upd properties

        description_prop = Property(name="http://127.0.0.1/ockb/course/ontology/description")
        begin_date_prop = Property(name="http://127.0.0.1/ockb/course/ontology/beginDate")
        end_date_prop = Property(name="http://127.0.0.1/ockb/course/ontology/endDate")
        requirement_prop = Property(name="http://127.0.0.1/ockb/course/ontology/requirement")
        duration_prop = Property(name="http://127.0.0.1/ockb/course/ontology/duration")
        cost_prop = Property(name="http://127.0.0.1/ockb/course/ontology/cost")
        teacher_name_prop = Property(name="http://127.0.0.1/ockb/course/ontology/teacherName")
        content_name_prop = Property(name="http://127.0.0.1/ockb/course/ontology/content")
        course_name_prop = Property(name="http://127.0.0.1/ockb/course/ontology/courseName")

        # db.session.add(description_prop)
        # db.session.add(begin_date_prop)
        # db.session.add(end_date_prop)
        # db.session.add(requirement_prop)
        # db.session.add(duration_prop)
        # db.session.add(cost_prop)
        # db.session.add(teacher_name_prop)
        # db.session.add(content_name_prop)
        # db.session.add(course_name_prop)

        # Setting up answers

        ObtenerInformacionAnswer = Answer(uri="ObtenerInformacionAnswer", answer_template="{%description%}",
                                          properties=[description_prop])

        # db.session.add(ObtenerInformacionAnswer)
        ObtenerFechasAnswer = Answer(uri="ObtenerFechasAnswer",
                                     answer_template="Las fechas importantes del curso son {%beginDate%} y termina el dia {%endDate%}",
                                     properties=[begin_date_prop, end_date_prop])

        # db.session.add(ObtenerFechasAnswer)
        ObtenerFechasInicioAnswer = Answer(uri="ObtenerFechasInicioAnswer",
                                           answer_template="El curso inicia el dia {%beginDate%}",
                                           properties=[begin_date_prop])
        # db.session.add(ObtenerFechasInicioAnswer)
        ObtenerFechasFinAnswer = Answer(uri="ObtenerFechasFinAnswer",
                                        answer_template="El curso finaliza el dia {%endDate%}",
                                        properties=[end_date_prop])
        # db.session.add(ObtenerFechasFinAnswer)
        ObtenerPrerequisitosAnswer = Answer(uri="ObtenerPrerequisitosAnswer",
                                            answer_template="Los prerequisitos del curso son {%requirement%}",
                                            properties=[requirement_prop])
        # db.session.add(ObtenerPrerequisitosAnswer)
        ObtenerDuracionAnswer = Answer(uri="ObtenerDuracionAnswer",
                                       answer_template="El curso tiene una duracion de {%duration%}",
                                       properties=[duration_prop])
        # db.session.add(ObtenerDuracionAnswer)
        ObtenerPrecioAnswer = Answer(uri="ObtenerPrecioAnswer", answer_template="{%cost%}", properties=[cost_prop])
        # db.session.add(ObtenerPrecioAnswer)
        ObtenerDocenteAnswer = Answer(uri="ObtenerDocenteAnswer",
                                      answer_template="El docente encargado del curso es {%teacherName%}",
                                      properties=[teacher_name_prop],
                                      refers_to="http://127.0.0.1/ockb/course/ontology/hasTeacher")
        # db.session.add(ObtenerDocenteAnswer)
        ObtenerContenidosAnswer = Answer(uri="ObtenerContenidosAnswer",
                                         answer_template="Los contenidos a tratar en el curso son {%content%}",
                                         properties=[content_name_prop],
                                         refers_to="http://127.0.0.1/ockb/course/ontology/hasContenido")
        # db.session.add(ObtenerContenidosAnswer)
        ListarCursosAnswer = Answer(uri="ListarCursosAnswer",
                                    answer_template="Los cursos de la oferta actual son: {%courseName%}",
                                    properties=[course_name_prop],
                                    refers_to="http://127.0.0.1/ockb/course/ontology/hasCourse",
                                    answer_from="http://127.0.0.1/ockb/resources/OpenCampusFebrero-Julio")

        # Setting up resolution
        ObtenerInformacionResolution = Resolution(uri="ObtenerInformacionResolution",
                                                  question="De que cursos deseas conocer",
                                                  resolves="http://127.0.0.1/ockb/course/resource/Course")
        ObtenerFechasResolution = Resolution(uri="ObtenerFechasResolution", question="De que cursos deseas conocer",
                                             resolves="http://127.0.0.1/ockb/course/resource/Course")
        ObtenerFechasInicioResolution = Resolution(uri="ObtenerFechasInicioResolution",
                                                   question="De que cursos deseas conocer",
                                                   resolves="http://127.0.0.1/ockb/course/resource/Course")
        ObtenerFechasFinResolution = Resolution(uri="ObtenerFechasFinResolution",
                                                question="De que cursos deseas conocer",
                                                resolves="http://127.0.0.1/ockb/course/resource/Course")
        ObtenerPrerequisitosResolution = Resolution(uri="ObtenerPrerequisitosResolution",
                                                    question="De que cursos deseas conocer",
                                                    resolves="http://127.0.0.1/ockb/course/resource/Course")
        ObtenerDuracionResolution = Resolution(uri="ObtenerDuracionResolution", question="De que cursos deseas conocer",
                                               resolves="http://127.0.0.1/ockb/course/resource/Course")
        ObtenerPrecioResolution = Resolution(uri="ObtenerPrecioResolution", question="De que cursos deseas conocer",
                                             resolves="http://127.0.0.1/ockb/course/resource/Course")
        ObtenerDocenteResolution = Resolution(uri="ObtenerDocenteResolution", question="De que cursos deseas conocer",
                                              resolves="http://127.0.0.1/ockb/course/resource/Course")
        ObtenerContenidosResolution = Resolution(uri="ObtenerContenidosResolution",
                                                 question="De que cursos deseas conocer",
                                                 resolves="http://127.0.0.1/ockb/course/resource/Course")

        # Setting up Entity

        curso_entity = Entity(name="http://127.0.0.1/ockb/course/resource/Course")

        # setting up synonyms:
        Synonym(name="Mooc", entity=curso_entity)
        Synonym(name="Taller", entity=curso_entity)
        Synonym(name="Curso", entity=curso_entity)
        Synonym(name="Open Course", entity=curso_entity)

        # Setting up intents

        ObtenerInformacion = Intent(name="ObtenerInformacion", agent=agent,
                                    description="Obtener una breve descripcion del curso",
                                    answer=ObtenerInformacionAnswer, resolution=ObtenerInformacionResolution,
                                    entities=[curso_entity])
        ObtenerFechas = Intent(name="ObtenerFechas", agent=agent,
                               description="Obtener las fechas importantes del curso",
                               answer=ObtenerFechasAnswer, resolution=ObtenerFechasResolution, entities=[curso_entity])
        ObtenerFechasInicio = Intent(name="ObtenerFechasInicio", agent=agent,
                                     description="Obtener las fechas de inicio del curso",
                                     answer=ObtenerFechasInicioAnswer, resolution=ObtenerFechasInicioResolution,
                                     entities=[curso_entity])
        ObtenerFechasFin = Intent(name="ObtenerFechasFin", agent=agent,
                                  description="Obtener las fechas de finalizacion del curso",
                                  answer=ObtenerFechasFinAnswer, resolution=ObtenerFechasFinResolution,
                                  entities=[curso_entity])
        ObtenerPrerequisitos = Intent(name="ObtenerPrerequisitos", agent=agent,
                                      description="Obtener prerequisitos del curso",
                                      answer=ObtenerPrerequisitosAnswer,
                                      resolution=ObtenerPrerequisitosResolution)
        ObtenerDuracion = Intent(name="ObtenerDuracion", agent=agent,
                                 description="Obtener la duracion del curso", answer=ObtenerDuracionAnswer,
                                 resolution=ObtenerDuracionResolution, entities=[curso_entity])
        ObtenerPrecio = Intent(name="ObtenerPrecio", agent=agent, description="Obtener el precio del curso",
                               answer=ObtenerPrecioAnswer, resolution=ObtenerPrecioResolution, entities=[curso_entity])
        ObtenerDocente = Intent(name="ObtenerDocente", agent=agent,
                                description="Obtener los nombres de los docentes del curso",
                                answer=ObtenerDocenteAnswer, resolution=ObtenerDocenteResolution,
                                entities=[curso_entity])
        ObtenerContenidos = Intent(name="ObtenerContenidos", agent=agent,
                                   description="Obtener los contenidos del curso",
                                   answer=ObtenerContenidosAnswer, resolution=ObtenerDocenteResolution,
                                   entities=[curso_entity])
        ListarCursos = Intent(name="ListarCursos", agent=agent,
                              description="Presentar la oferta actual de cursos", answer=ListarCursosAnswer,
                              resolution=ObtenerContenidosResolution)
        # Setting up sentences

        Sentence(intent=ObtenerInformacion, sentence="De que trata el mooc?")
        Sentence(intent=ObtenerInformacion, sentence="Quiero informacion del curso de emprendimiento")
        Sentence(intent=ObtenerInformacion, sentence="Muestrame un resumen del mooc?")
        Sentence(intent=ObtenerInformacion, sentence="Breve introducción al curso")
        Sentence(intent=ObtenerInformacion, sentence="que es emprendimiento")
        Sentence(intent=ObtenerInformacion, sentence="De que se trata el curso?")
        Sentence(intent=ObtenerInformacion, sentence="De qué va el curso?")
        Sentence(intent=ObtenerInformacion, sentence="Me ayudas con información acerca del curso?")
        Sentence(intent=ObtenerFechas, sentence="Cuáles son las fechas importantes del curso?")
        Sentence(intent=ObtenerFechas, sentence="Fechas clave del curso")
        Sentence(intent=ObtenerFechas, sentence="Que fechas debo tomar en cuenta")
        Sentence(intent=ObtenerFechas, sentence="fechas de inicio y fin")
        Sentence(intent=ObtenerFechas, sentence="Cuándo comienza el curso?")
        Sentence(intent=ObtenerFechas, sentence="Fechas importantes del curso de inteligencia artificial")
        Sentence(intent=ObtenerFechas, sentence="Cuáles son las fechas importantes del curso de emprendimiento")
        Sentence(intent=ObtenerFechasInicio, sentence="Cuándo inicia el curso de emprendimiento")
        Sentence(intent=ObtenerFechasInicio, sentence="Cuándo empiezan los cursos ?")
        Sentence(intent=ObtenerFechasInicio, sentence="Fecha de inicio de los moocs?")
        Sentence(intent=ObtenerFechasInicio, sentence="Día de inicio de los moocs ?")
        Sentence(intent=ObtenerFechasInicio, sentence="En que fecha inician los moocs?")
        Sentence(intent=ObtenerFechasInicio, sentence="A partir de que fecha empiezan los mooc?")
        Sentence(intent=ObtenerFechasFin, sentence="Cuando finaliza el curso?")
        Sentence(intent=ObtenerFechasFin, sentence="En que fecha termina el curso?")
        Sentence(intent=ObtenerFechasFin, sentence="Cuando termina el curso?")
        Sentence(intent=ObtenerPrerequisitos,
                 sentence="Cuáles son los requisitos necesarios para el curso de emprendimiento")
        Sentence(intent=ObtenerPrerequisitos, sentence="Cuáles son los prerequisitos?")
        Sentence(intent=ObtenerPrerequisitos, sentence="Requisitos previos de ingreso  al curso")
        Sentence(intent=ObtenerPrerequisitos, sentence="Dame a conocer los prerequisitos")
        Sentence(intent=ObtenerPrerequisitos, sentence="Me puedes indicar los prerequistos necesarios?")
        Sentence(intent=ObtenerPrerequisitos, sentence="Que necesito saber antes de iniciar el curso")
        Sentence(intent=ObtenerPrerequisitos, sentence="que se necesita saber para este curso")
        Sentence(intent=ObtenerPrerequisitos, sentence="Los pre requisitos  cuales son?")
        Sentence(intent=ObtenerPrerequisitos, sentence="Qué se necesita?")
        Sentence(intent=ObtenerPrerequisitos, sentence="Qué debería saber para tomar el curso?")
        Sentence(intent=ObtenerPrerequisitos, sentence="Qué conocimientos previos debo tener?")
        Sentence(intent=ObtenerPrerequisitos, sentence="Qué tengo que saber?")
        Sentence(intent=ObtenerPrerequisitos, sentence="Requisitos previos")
        Sentence(intent=ObtenerPrerequisitos, sentence="Conocimientos previos")
        Sentence(intent=ObtenerDuracion, sentence="Cuanto dura el curso de empendimiento")
        Sentence(intent=ObtenerDuracion, sentence="Duración del curso")
        Sentence(intent=ObtenerDuracion, sentence="Número de horas del mooc?")
        Sentence(intent=ObtenerDuracion, sentence="En cuántas semanas se realiza el curso?")
        Sentence(intent=ObtenerDuracion, sentence="Cuanto dura el curso")
        Sentence(intent=ObtenerDuracion, sentence="Tiempo que dura un curso?")
        Sentence(intent=ObtenerDuracion, sentence="cuanto puede durar un curso mooc")
        Sentence(intent=ObtenerDuracion, sentence="cuanto dura el curso?")
        Sentence(intent=ObtenerDuracion, sentence="cual es la duracion de psicologia social?")
        Sentence(intent=ObtenerDuracion, sentence="Cuánto tiempo dura el mooc?")
        Sentence(intent=ObtenerDuracion, sentence="De cuántas semanas es el mooc?")
        Sentence(intent=ObtenerDuracion, sentence="Cuántas horas dura el mooc?")
        Sentence(intent=ObtenerDuracion, sentence="Cuánto tiempo dura el mooc?")
        Sentence(intent=ObtenerDuracion, sentence="De cuántas semanas es el mooc?")
        Sentence(intent=ObtenerPrecio, sentence="Cual es el precio del curso de emprendimiento")
        Sentence(intent=ObtenerPrecio, sentence="Cuál es el precio?")
        Sentence(intent=ObtenerPrecio, sentence="Cuánto vale?")
        Sentence(intent=ObtenerPrecio, sentence="Valor del curso?")
        Sentence(intent=ObtenerPrecio, sentence="Costo")
        Sentence(intent=ObtenerPrecio, sentence="Inversión total del curso")
        Sentence(intent=ObtenerPrecio, sentence="cual es el valor de los componentes?")
        Sentence(intent=ObtenerPrecio, sentence="costo de los cursos?")
        Sentence(intent=ObtenerPrecio, sentence="cuanto cuesta los cursos")
        Sentence(intent=ObtenerPrecio, sentence="Cuál es precio del curso?")
        Sentence(intent=ObtenerPrecio, sentence="Cuánto cuesta el mooc de Administración Empresarial?")
        Sentence(intent=ObtenerPrecio, sentence="tiene algun valor los cursos?")
        Sentence(intent=ObtenerPrecio, sentence="Cuanto cuesta el  curso Método Toyota?")
        Sentence(intent=ObtenerPrecio, sentence="Cuanto cuesta un curso?")
        Sentence(intent=ObtenerPrecio, sentence="Que vale el curso ?")
        Sentence(intent=ObtenerPrecio, sentence="Es gratis?")
        Sentence(intent=ObtenerPrecio, sentence="Cuanto vale el mooc?")
        Sentence(intent=ObtenerPrecio, sentence="Precio")
        Sentence(intent=ObtenerDocente, sentence="Cual es el docente del curso de emprendimiento")
        Sentence(intent=ObtenerDocente, sentence="Quién es mi profesor en el curso?")
        Sentence(intent=ObtenerDocente, sentence="Docente del mooc?")
        Sentence(intent=ObtenerDocente, sentence="Qué docente imparte el mooc?")
        Sentence(intent=ObtenerDocente, sentence="Quién es el docente encargado de la materia?")
        Sentence(intent=ObtenerDocente, sentence="Nombre del docente del mooc")
        Sentence(intent=ObtenerDocente, sentence="Que profesor esta a cargo del curso")
        Sentence(intent=ObtenerDocente, sentence="cual es mi docente del mooc")
        Sentence(intent=ObtenerDocente, sentence="información del docente")
        Sentence(intent=ObtenerDocente, sentence="Quién es el docente encargado?")
        Sentence(intent=ObtenerDocente, sentence="Quién va a dar el MOOC")
        Sentence(intent=ObtenerDocente, sentence="Que docente acompaña  al estudiante?")
        Sentence(intent=ObtenerDocente, sentence="Cual es el profe de Salud Sexual y Reproductiva")
        Sentence(intent=ObtenerContenidos, sentence="Cuáles son los contenidos a tratar en el curos de emprendimiento")
        Sentence(intent=ObtenerContenidos, sentence="Contenido del curso")
        Sentence(intent=ObtenerContenidos, sentence="Cuál es la temática de cada curso?")
        Sentence(intent=ObtenerContenidos, sentence="Qué temas se van a tratar en cada curso?")
        Sentence(intent=ObtenerContenidos, sentence="De que se tratan los moocs")
        Sentence(intent=ObtenerContenidos, sentence="Cuáles son las temas del curso?")
        Sentence(intent=ObtenerContenidos, sentence="Que se va a tratar en este curso?")
        Sentence(intent=ObtenerContenidos, sentence="Qué se va a dar en el curso?")
        Sentence(intent=ListarCursos, sentence="Que cursos hay")
        Sentence(intent=ListarCursos, sentence="Muestrame los cursos")
        Sentence(intent=ListarCursos, sentence="Cual es la oferta actual")
        Sentence(intent=ListarCursos, sentence="Cuentame que cursos tienes")
        Sentence(intent=ListarCursos, sentence="Que cursos me ofreces")
        Sentence(intent=ListarCursos, sentence="Que cursos estan disponibles")
        Sentence(intent=ListarCursos, sentence="Listame los cursos")
        Sentence(intent=ListarCursos, sentence="Que cursos tiene")

        # db.session.add(intent_obtenerinformacion)
        # db.session.add(intent_obtenerfechas)
        # db.session.add(intent_obtenerfechasinicio)
        # db.session.add(intent_obtenerfechasfin)
        # db.session.add(intent_obtenerprerequisitos)
        # db.session.add(intent_obtenerduracion)
        # db.session.add(intent_obtenerprecio)
        # db.session.add(intent_obtenerdocente)
        # db.session.add(intent_obtenercontenidos)
        # db.session.add(intent_listarCursos)

        db.session.commit()
