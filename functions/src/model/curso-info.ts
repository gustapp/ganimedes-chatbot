import { WebhookClient } from 'dialogflow-fulfillment';
import { DataAccessHelper } from '../dao/data-access-base';

export class CursoInfo {

    constructor(private db: FirebaseFirestore.Firestore){};

    /**
     * @function getCourse
     * @param agent 
     */
    public getCourse(agent: WebhookClient) {
        const course = agent.parameters.Course;

        let dbHelper = new DataAccessHelper(this.db.collection('cursos'));
        return dbHelper.doc(course).then(doc => {
            if(doc){
                agent.add("O que você gostaria de saber sobre essa disciplina? Talvez a descrição da disciplina, ou os horários?");
            }
            else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        })
        .catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }
    /**
     * @function getCourseInfo
     * @param agent
     */
    public getCourseInfo(agent: WebhookClient) {
        const course = agent.parameters.Course;
        let dbHelper = new DataAccessHelper(this.db.collection('cursos'));

        return dbHelper.doc(course).then(result => {
            if(result){
                agent.add(`A disciplina ${course} - ${result.name} possui a seguinte descrição: ${result.objetivos}`);
            }
            else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        })
        .catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }
    /**
     * @function getCourseRequirements
     * @param agent 
     */
    public getCourseRequirements(agent: WebhookClient) {
        const course = agent.parameters.Course;

        let dbHelper = new DataAccessHelper(this.db.collection('cursos'));
        return dbHelper.doc(course).then(result => {
            if (result) {
                if(result.requisitos.length > 0){
                    agent.add(`A disciplina possui os seguintes requisitos: ${result.requisitos.join(',')}`);
                }
                else {
                    agent.add("A disciplina não possui requisitos!")
                }
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        }).catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }
    /**
     * @function getCourseWorkload
     * @param agent
     */
    public getCourseWorkload(agent: WebhookClient) {
        const course = agent.parameters.Course;

        let dbHelper = new DataAccessHelper(this.db.collection('cursos'));
        return dbHelper.doc(course).then(result => {
            if (result) {
                agent.add(`A disciplina possui ${result.carga_horaria} horas por semestre!`);
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        }).catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }
    /**
     * @function getCourseTeacher
     * @param agent
     */
    public getCourseTeacher(agent: WebhookClient) {
        const course = agent.parameters.Course;

        let dbHelper = new DataAccessHelper(this.db.collection('cursos'));
        return dbHelper.doc(course).then(result => {
            if (result) {
                if(result.docentes.length > 0){
                    agent.add(`A disciplina possui os seguintes professores: ${result.docentes.join(',')}`);
                }
                else {
                    agent.add("A disciplina não possui nenhum professor cadastrado no sistema!");
                }
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        }).catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }

    /**
     * @function getCourseSchedule
     * @param agent
     */
    public getCourseSchedule(agent: WebhookClient) {
        const course = agent.parameters.Course;
        
        const courseRef = this.db.collection('cursos'); 

        let coursePr = new DataAccessHelper(courseRef).doc(course);

        return coursePr.then(courseRes => {
            if(courseRes){
                const offersRef = courseRef.doc(courseRes.sigla).collection('oferecimentos');

                let offersPr = new DataAccessHelper(offersRef).coll();

                return offersPr.then(offers => {

                    return Promise.all<temp>(

                        offers.map(offer => {
                            const class_code = offer.codigo_turma.toString().slice(-2);
    
                            const schedulesRef = offersRef.doc(offer.codigo_turma).collection("horarios");
                            
                            let schedulesPr = new DataAccessHelper(schedulesRef).coll();

                            return schedulesPr.then(schedules => {

                                // model
                                return {
                                    class_code: class_code,
                                    schedules: schedules
                                };
                            })
                        })
                    )
                    .then(class_schedules => {
                        // view-model
                        let messageBuilder = [];
                        class_schedules.forEach(class_schedule => {
                            messageBuilder.push(`--> A turma ${class_schedule.class_code} tem os seguintes horários: /\n/`);

                            class_schedule.schedules.forEach(schedule => {
                                messageBuilder.push(`-> ${schedule.dia} às ${schedule.horario_inicio} - ${schedule.horario_fim}\n`);
                            });
                        });

                        agent.add(`${messageBuilder.join('')}`)
                    });
                });
            }
            else {
                agent.add("Desculpe, não encontrei a disciplina.");
                return void[];
            }
        })
        .catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }

    /**
     * @function getCourseCredit
     * @param agent
     */
    public getCourseCredit(agent: WebhookClient) {
        const course = agent.parameters.Course;
        let dbHelper = new DataAccessHelper(this.db.collection('cursos'));
        return dbHelper.doc(course).then(result => {
            if (result) {
                agent.add(`São ${result.creditos.aula} créditos aula e ${result.creditos.trabalho} créditos trabalho`);
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        }).catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }
    /**
     * @function getCourseFromScheduleDay
     * @param agent
     */
    public getCourseFromScheduleDay(agent: WebhookClient) {
        agent.add(`getCourseFromScheduleDay 🔥`);
    }
    /**
     * @function getCourseFromScheduleDayHour
     * @param agent
     */
    public getCourseFromScheduleDayHour(agent: WebhookClient) {
        agent.add(`getCourseFromScheduleDayHour 🔥`);
    }
    /**
     * @function fallbackGetCourseId2
     * @param agent
     */
    public fallbackGetCourseId2(agent: WebhookClient) {
        agent.add(`fallbackGetCourseId2 🔥`);
    }
}

interface temp {
    class_code: any,
    schedules: any[]
}
