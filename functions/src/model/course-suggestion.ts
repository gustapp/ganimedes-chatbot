import { WebhookClient } from 'dialogflow-fulfillment';
const axios = require("axios");
// const request = require("request-promise-native");

export class CourseSuggestion {

    constructor(db: FirebaseFirestore.Firestore){};

    /**
     * @function getCourseSuggestion
     * @param agent 
     */
    public async getCourseSuggestion(agent: WebhookClient) {
        const empty = "indiferente";
        const theme = agent.parameters.theme;
        const weekdays = agent.parameters.weekdays;
        const teachers : any[] = agent.parameters.teachers;
        const max = agent.parameters.suggestion_number;
        const period = agent.parameters.time_period;

        const url = `https://us-central1-ganimedes-d9ecd.cloudfunctions.net/course-suggestion?message=${theme}`;

        try {
            const response = await axios.get(url);
            if(response){
                const data = response.data;
                agent.add(`Eu te recomendo o artigo ${data[0]}`)
            }
            else {
                agent.add(`Desculpe, não achei nada interessante...`)
            }
        } catch (error) {
            agent.add("Desculpe, houve um erro na aplicação. Tente novamente");
        }
    }
}