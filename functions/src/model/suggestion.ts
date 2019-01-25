import { WebhookClient } from 'dialogflow-fulfillment';

export class Suggestion {

    constructor(private db: FirebaseFirestore.Firestore){};

    /**
     * @function getCourseSuggestion
     * @param agent 
     */
    public getCourseSuggestion(agent: WebhookClient) {
        const empty = "indiferente";
        const theme = agent.parameters.theme;
        const weekdays = agent.parameters.weekdays;
        const teachers : any[] = agent.parameters.teachers;
        const max = agent.parameters.suggestion_number;
        const period = agent.parameters.time_period;

        const collRef = this.db.collection('cursos');

        // if(period){
        //     collRef.where("oferecimento")
        // }

        // if(teachers[0] != empty){
        //     teachers.forEach(teacher => {
        //         let teacherQuery = collRef.where('docentes', 'array-contains', teacher).limit(max)
        //     });
        // }

        // return collRef.where('').limit(max).get().then(doc => {
        //     if (doc.exists) {
        //         agent.add("O que você gostaria de saber sobre essa disciplina? Talvez a descrição da disciplina, ou os horários?");
        //     } else {
        //         agent.add("Desculpe, não encontrei a disciplina.");
        //     }
        // }).catch(error => {
        //     agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        // });
    }
}