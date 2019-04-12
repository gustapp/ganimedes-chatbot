import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

import { WebhookClient } from 'dialogflow-fulfillment';
import { HandlerFacade } from './handler-facade';

process.env.DEBUG = 'dialogflow:debug';

admin.initializeApp(functions.config().firebase);

/**
 * @function helloWorld
 * Test function
 */
export const helloWorld = functions.https.onRequest((request, response) => {
    response.send("Hello! Lets chat! lol");
});

/**
 * @function dialogflowFirebaseFulfillment
 * Dialogue fulfillment function for ganimedes chatbot
 */
export const dialogflowFirebaseFulfillment = functions.https.onRequest((request, response) => {
    const agent = new WebhookClient({ request, response });
    console.log('Dialogflow Request headers: ' + JSON.stringify(request.headers));
    console.log('Dialogflow Request body: ' + JSON.stringify(request.body));

    // Retrieve firestore
    const db = admin.firestore();
    // const settings = { timestampsInSnapshots: true };
    // db.settings(settings);

    // RepositoryFactory.getInstance(db);

    const facade = new HandlerFacade(db);

    // Run the proper function handler based on the matched Dialogflow intent name
    const intentMap = new Map();

    // Test intents
    intentMap.set('Welcome', facade.welcome);
    intentMap.set('Fallback', facade.fallback);
    intentMap.set('Test', facade.yourFunction);

    // Jupiter intents
    intentMap.set('fallbackGetCourseId2', facade.fallbackGetCourseId2);
    intentMap.set('getCourse', (client) => facade.getCourse(client));
    intentMap.set('GetCourseInfo', (client) => facade.getCourseInfo(client));
    intentMap.set('GetCourseRequirements', (client) => facade.getCourseRequirements(client));
    intentMap.set('GetCourseWorkload', (client) => facade.getCourseWorkload(client));
    intentMap.set('GetCourseTeacher', (client) => facade.getCourseTeacher(client));
    intentMap.set('GetCourseSchedule', (client) => facade.getCourseSchedule(client));
    intentMap.set('GetCourseCredit', (client) => facade.getCourseCredit(client));
    intentMap.set('getCourseFromScheduleDay', (client) => facade.getCourseFromScheduleDay(client)); 
    intentMap.set('getCourseFromScheduleDayHour', (client) => facade.getCourseFromScheduleDayHour(client));
    intentMap.set('GetCourseSuggestion', (client) => facade.getCourseSuggestion(client));

    agent.handleRequest(intentMap);
});