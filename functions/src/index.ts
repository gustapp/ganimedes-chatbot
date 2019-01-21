import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

import { WebhookClient } from 'dialogflow-fulfillment';
import { HandlerFacade } from './handler-facade';

process.env.DEBUG = 'dialogflow:debug';

admin.initializeApp(functions.config().firebase);
const db = admin.firestore();

const facade = new HandlerFacade(db);

/**
 * @function helloWorld
 * Test function
 */
export const helloWorld = functions.https.onRequest((request, response) => {
    response.send("Hello! Lets chat!");
});

/**
 * @function dialogflowFirebaseFulfillment
 * Dialogue fulfillment function for ganimedes chatbot
 */
export const dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
    const agent = new WebhookClient({ request, response });
    console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
    console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

    // Run the proper function handler based on the matched Dialogflow intent name
    const intentMap = new Map();

    // Test intents
    intentMap.set('Welcome', facade.welcome);
    intentMap.set('Fallback', fallback);
    intentMap.set('Test', yourFunction);

    // Jupiter intents
    intentMap.set('fallbackGetCourseId2', fallbackGetCourseId2);
    intentMap.set('getCourse', getCourse);
    intentMap.set('GetCourseInfo', getCourseInfo); //ok
    intentMap.set('GetCourseRequirements', getCourseRequirements); //ok
    intentMap.set('GetCourseWorkload', getCourseWorkload); //ok
    intentMap.set('GetCourseTeacher', getCourseTeacher); //ok
    intentMap.set('GetCourseSchedule', getCourseSchedule); //ok
    intentMap.set('GetCourseCredit', getCourseCredit); //ok
    intentMap.set('getCourseFromScheduleDay', getCourseFromScheduleDay);
    intentMap.set('getCourseFromScheduleDayHour', getCourseFromScheduleDayHour);
    intentMap.set('getCourseSuggestion', getCourseSuggestion);
    intentMap.set('getCourseSuggestionBefore', getCourseSuggestionBefore);
    intentMap.set('getCourseSuggestionAfter', getCourseSuggestionAfter);
    intentMap.set('getCourseSuggestionBetween', getCourseSuggestionBetween);
    intentMap.set('getCourseSuggestionDays', getCourseSuggestionDays);

    agent.handleRequest(intentMap);
});