import * as functions from 'firebase-functions';
import { WebhookClient } from 'dialogflow-fulfillment';

import { welcome } from './handlers/welcome.handler';
import { fallback } from './handlers/fallback.handler';
import { yourFunction } from './handlers/test.handler';

process.env.DEBUG = 'dialogflow:debug';

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
    intentMap.set('Default Welcome Intent', welcome);
    intentMap.set('Default Fallback Intent', fallback);
    intentMap.set('Default Test Intent', yourFunction);
    agent.handleRequest(intentMap);
});