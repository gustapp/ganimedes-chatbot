import { WebhookClient } from 'dialogflow-fulfillment';
import { RepositoryFactory } from '../data-access/repository-factory';
import { CourseRepository } from '../data-access/course-repository';
// import { ClassRepository  } from '../data-access/class-repository'
// import { ScheduleRepository } from '../data-access/schedule-repository'

export class CursoInfo {

    private repoFactory: RepositoryFactory;

    constructor(db: FirebaseFirestore.Firestore){
        this.repoFactory = new RepositoryFactory(db);
    };

    /**
     * @function getCourse
     * @param agent 
     */
    public async getCourse(agent: WebhookClient) {
        try {
            const courseId = agent.parameters.Course;
            const courseRepo = this.repoFactory.create(CourseRepository);

            const course = await courseRepo.get(courseId);

            if(course){
                agent.add("O que você gostaria de saber sobre essa disciplina? Talvez a descrição da disciplina, ou os horários?");
            }
            else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }            
        } catch (error) {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        }
    }
    /**
     * @function getCourseInfo
     * @param agent
     */
    public async getCourseInfo(agent: WebhookClient) {
        try {
            const courseId = agent.parameters.Course;
            const courseRepo = this.repoFactory.create(CourseRepository);

            const result = await courseRepo.get(courseId);

            if(result){
                agent.add(`A disciplina ${courseId} - ${result.name} possui a seguinte descrição: ${result.objectives}`);
            }
            else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        } catch (error) {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        }
    }
    /**
     * @function getCourseRequirements
     * @param agent 
     */
    public async getCourseRequirements(agent: WebhookClient) {
        try {
            const courseId = agent.parameters.Course;
            const courseRepo = this.repoFactory.create(CourseRepository);

            const result = await courseRepo.get(courseId);

            if (result) {
                if(result.requirements.length > 0){
                    agent.add(`A disciplina possui os seguintes requisitos: ${result.requirements.join(',')}`);
                }
                else {
                    agent.add("A disciplina não possui requisitos!")
                }
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }            
        } catch (error) {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        }
    }
    /**
     * @function getCourseWorkload
     * @param agent
     */
    public async getCourseWorkload(agent: WebhookClient) {
        try {
            const courseId = agent.parameters.Course;
            const courseRepo = this.repoFactory.create(CourseRepository);

            const result = await courseRepo.get(courseId);

            if (result) {
                agent.add(`A disciplina possui ${result.workload} horas por semestre!`);
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        } catch (error) {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        }
    }
    /**
     * @function getCourseTeacher
     * @param agent
     */
    public async getCourseTeacher(agent: WebhookClient) {
        try {
            const courseId = agent.parameters.Course;
            const courseRepo = this.repoFactory.create(CourseRepository);

            const result = await courseRepo.get(courseId);

            if (result) {
                if(result.teachers.length > 0){
                    agent.add(`A disciplina possui os seguintes professores: ${result.teachers.join(',')}`);
                }
                else {
                    agent.add("A disciplina não possui nenhum professor cadastrado no sistema!");
                }
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        } catch (error) {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        }
    }

    /**
     * @function getCourseSchedule
     * @param agent
     */
    public async getCourseSchedule(agent: WebhookClient) {
        try {
            const courseId = agent.parameters.Course;
            const courseRepo = this.repoFactory.create(CourseRepository);

            const course = await courseRepo.get(courseId);

            if(course){

                const classes = await course.getClasses();

                const messageBuilder = [];
                for(const offer of classes){
                    const classCode = offer.code.toString().slice(-2);

                    messageBuilder.push(`--> A turma ${classCode} tem os seguintes horários: /\n/`);

                    const schedules = await offer.getSchedules();
                    schedules.forEach(schedule => {
                        messageBuilder.push(`-> ${schedule.weekday} às ${schedule.start} - ${schedule.end}\n`);
                    });
                }

                agent.add(`${messageBuilder.join('')}`);
            }
            else {
                agent.add("Desculpe, não encontrei a disciplina.");
                return void[];
            }

        } catch (error) {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        }
    }

    /**
     * @function getCourseCredit
     * @param agent
     */
    public async getCourseCredit(agent: WebhookClient) {
        try {
            const courseId = agent.parameters.Course;
            const courseRepo = this.repoFactory.create(CourseRepository);

            const result = await courseRepo.get(courseId);
            
            if (result) {
                agent.add(`São ${result.credits.aula} créditos aula e ${result.credits.trabalho} créditos trabalho`);
            } else {
                agent.add("Desculpe, não encontrei a disciplina.");
            }
        } catch (error) {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        }
    }
    /**
     * @function getCourseFromScheduleDay
     * @param agent
     */
    public getCourseFromScheduleDay(agent: WebhookClient) {
        agent.add(`TODO getCourseFromScheduleDay 🔥`);
    }
    /**
     * @function getCourseFromScheduleDayHour
     * @param agent
     */
    public getCourseFromScheduleDayHour(agent: WebhookClient) {
        agent.add(`TODO getCourseFromScheduleDayHour 🔥`);
    }
    /**
     * @function fallbackGetCourseId2
     * @param agent
     */
    public fallbackGetCourseId2(agent: WebhookClient) {
        agent.add(`TODO fallbackGetCourseId2 🔥`);
    }
}

// interface temp {
//     class_code: any,
//     schedules: any[]
// }
