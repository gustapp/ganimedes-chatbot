import { WebhookClient } from 'dialogflow-fulfillment';

export const welcome = function welcomeHandler(agent: WebhookClient) {
    agent.add(`Hello! Lets chat 🔥`);
};