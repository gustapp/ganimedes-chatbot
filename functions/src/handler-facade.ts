import { WebhookClient, Card, Suggestion } from 'dialogflow-fulfillment';
import { CursoInfo } from './model/curso-info';
/**
 * @class
 * Facade for all handlers
 */
export class HandlerFacade {

    // private refFactory: ReferenceFactory;
    private cursoInfo: CursoInfo;
    /**
     * @constructor
     * @param db firestore manager
     */
    constructor(db: FirebaseFirestore.Firestore){
        // this.refFactory = new ReferenceFactory(db);
        this.cursoInfo = new CursoInfo(db);
    }
    /**
     * @function welcome
     * @param agent 
     */
    public welcome(agent: WebhookClient) {
        agent.add(`Hello! Lets chat 🔥`);
    }
    /**
     * @function fallback
     * @param agent 
     */
    public fallback(agent: WebhookClient) {
        agent.add(`I didn't understand`);
        agent.add(`I'm sorry, can you try again?`);
    }
    /**
     * @function yourFunction
     * @param agent 
     */
    public yourFunction(agent: WebhookClient) {
        agent.add(`This message is from Dialogflow's Cloud Functions for Firebase editor!`);
        agent.add(new Card({
            title: `Title: this is a card title`,
            imageUrl: 'https://developers.google.com/actions/images/badges/XPM_BADGING_GoogleAssistant_VER.png',
            text: `This is the body text of a card.  You can even use line\n  breaks and emoji! 💁`,
            buttonText: 'This is a button',
            buttonUrl: 'https://assistant.google.com/'
          })
        );
        agent.add(new Suggestion(`Quick Reply`));
        agent.add(new Suggestion(`Suggestion`));
        agent.setContext({ name: 'weather', lifespan: 2, parameters: { city: 'Rome' }});
    }
    /**
     * @function getCourse
     * @param agent 
     */
    public getCourse(agent: WebhookClient) {
        return this.cursoInfo.getCourse(agent);
    }
    /**
     * @function getCourseInfo
     * @param agent
     */
    public getCourseInfo(agent: WebhookClient) {
        return this.cursoInfo.getCourseInfo(agent);
    }
    /**
     * @function getCourseRequirements
     * @param agent 
     */
    public getCourseRequirements(agent: WebhookClient) {
        return this.cursoInfo.getCourseRequirements(agent);
    }
    /**
     * @function getCourseWorkload
     * @param agent
     */
    public getCourseWorkload(agent: WebhookClient) {
        return this.cursoInfo.getCourseWorkload(agent);
    }
    /**
     * @function getCourseTeacher
     * @param agent
     */
    public getCourseTeacher(agent: WebhookClient) {
        return this.cursoInfo.getCourseTeacher(agent);
    }
    /**
     * @function getCourseSchedule
     * @param agent
     */
    public getCourseSchedule(agent: WebhookClient) {
        return this.cursoInfo.getCourseSchedule(agent);
    }
    /**
     * @function getCourseCredit
     * @param agent
     */
    public getCourseCredit(agent: WebhookClient) {
        return this.cursoInfo.getCourseCredit(agent);
    }
    /**
     * @function getCourseFromScheduleDay
     * @param agent
     */
    public getCourseFromScheduleDay(agent: WebhookClient) {
        this.cursoInfo.getCourseFromScheduleDay(agent);
    }
    /**
     * @function getCourseFromScheduleDayHour
     * @param agent
     */
    public getCourseFromScheduleDayHour(agent: WebhookClient) {
        this.cursoInfo.getCourseFromScheduleDayHour(agent);
    }
    /**
     * @function fallbackGetCourseId2
     * @param agent
     */
    public fallbackGetCourseId2(agent: WebhookClient) {
        this.cursoInfo.fallbackGetCourseId2(agent);
    }
    /**
     * @function getCourseSuggestion
     * @param agent
     */
    public getCourseSuggestion(agent: WebhookClient) {
        agent.add(`getCourseSuggestion 🔥`);
    }
    /**
     * @function getCourseSuggestionBefore
     * @param agent
     */
    public getCourseSuggestionBefore(agent: WebhookClient) {
        agent.add(`getCourseSuggestionBefore 🔥`);
    }
    /**
     * @function getCourseSuggestionAfter
     * @param agent
     */
    public getCourseSuggestionAfter(agent: WebhookClient) {
        agent.add(`getCourseSuggestionAfter 🔥`);
    }
    /**
     * @function getCourseSuggestionBetween
     * @param agent
     */
    public getCourseSuggestionBetween(agent: WebhookClient) {
        agent.add(`getCourseSuggestionBetween 🔥`);
    }
    /**
     * @function getCourseSuggestionDays
     * @param agent
     */
    public getCourseSuggestionDays(agent: WebhookClient) {
        agent.add(`getCourseSuggestionDays 🔥`);
    }
}