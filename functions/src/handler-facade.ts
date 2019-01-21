import { WebhookClient, Card, Suggestion } from 'dialogflow-fulfillment';
import { EntityFactory } from './entity-factory';
/**
 * @class
 * Facade for all handlers
 */
export class HandlerFacade {

    private entityFactory: EntityFactory;
    /**
     * @constructor
     * @param db firestore manager
     */
    constructor(db: FirebaseFirestore.Firestore){
        this.entityFactory = new EntityFactory(db);
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
        
    }
    /**
     * @function getCourseInfo
     * @param agent
     */
    public getCourseInfo(agent: WebhookClient) {

    }
    /**
     * @function getCourseRequirements
     * @param agent 
     */
    public getCourseRequirements(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseWorkload
     * @param agent
     */
    public getCourseWorkload(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseTeacher
     * @param agent
     */
    public getCourseTeacher(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseSchedule
     * @param agent
     */
    public getCourseSchedule(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseCredit
     * @param agent
     */
    public getCourseCredit(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseFromScheduleDay
     * @param agent
     */
    public getCourseFromScheduleDay(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseFromScheduleDayHour
     * @param agent
     */
    public getCourseFromScheduleDayHour(agent: WebhookClient) {
        
    }
    /**
     * @function fallbackGetCourseId2
     * @param agent
     */
    public fallbackGetCourseId2(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseSuggestion
     * @param agent
     */
    public getCourseSuggestion(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseSuggestionBefore
     * @param agent
     */
    public getCourseSuggestionBefore(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseSuggestionAfter
     * @param agent
     */
    public getCourseSuggestionAfter(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseSuggestionBetween
     * @param agent
     */
    public getCourseSuggestionBetween(agent: WebhookClient) {
        
    }
    /**
     * @function getCourseSuggestionDays
     * @param agent
     */
    public getCourseSuggestionDays(agent: WebhookClient) {
        
    }
}