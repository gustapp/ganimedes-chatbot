import { WebhookClient } from 'dialogflow-fulfillment';

export class CursoInfo {

    constructor(private db: FirebaseFirestore.Firestore){};

    /**
     * @function getCourse
     * @param agent 
     */
    public getCourse(agent: WebhookClient) {
        const course = agent.parameters.Course;
        const docRef = this.db.collection('cursos').doc(course);
        return docRef.get().then(doc => {
            if (doc.exists) {
                agent.add("O que você gostaria de saber sobre essa disciplina? Talvez a descrição da disciplina, ou os horários?");
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }        
        }).catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }
    /**
     * @function getCourseInfo
     * @param agent
     */
    public getCourseInfo(agent: WebhookClient) {
        const course = agent.parameters.Course;
        const docRef = this.db.collection('cursos').doc(course);
        return docRef.get().then(doc => {
            if (doc.exists) {
                const result = doc.data();
                agent.add(`A disciplina ${course} - ${result.name} possui a seguinte descrição: ${result.objetivos}`);
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        }).catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }
    /**
     * @function getCourseRequirements
     * @param agent 
     */
    public getCourseRequirements(agent: WebhookClient) {
        const course = agent.parameters.Course;
        const docRef = this.db.collection('cursos').doc(course);
        return docRef.get().then(doc => {
            if (doc.exists) {
                const result = doc.data();
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
        const docRef = this.db.collection('cursos').doc(course);
        return docRef.get().then(doc => {
            if (doc.exists) {
                const result = doc.data();
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
        const docRef = this.db.collection('cursos').doc(course);
        return docRef.get().then(doc => {
            if (doc.exists) {
                const result = doc.data();
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
        const docRef = this.db.collection('cursos').doc(course);
        return docRef.get().then(doc => {
            if (doc.exists) {
                const result = doc.data();
                if(result.oferecimento.length > 0){
                    const schedule_list = result.oferecimento;
                    let answer = "";

                    schedule_list.forEach(schedule => {
                        const class_code = schedule.codigo_turma.toString().slice(-2);
                        const class_schedule_list = schedule.horario;
    
                        answer += `A turma ${class_code} tem horário `;
    
                        class_schedule_list.forEach(class_schedule => {
                            answer += `${class_schedule.dia} às ${class_schedule.horario_inicio} - ${class_schedule.horario_fim} `;
                        });
    
                        answer += '. ';                 
                    });

                    agent.add(`${answer}`);
                }
                else {
                    agent.add("A disciplina não é oferecida neste semestre!");
                }
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        }).catch(error => {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        });
    }
    /**
     * @function getCourseCredit
     * @param agent
     */
    public getCourseCredit(agent: WebhookClient) {
        const course = agent.parameters.Course;
        const docRef = this.db.collection('cursos').doc(course);
        return docRef.get().then(doc => {
            if (doc.exists) {
                const result = doc.data();
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