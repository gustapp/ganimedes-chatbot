import { helloWorld } from "../src/index";
import {} from "ts-jest";

import * as chai from "chai";
const expect = chai.expect;

import * as request from 'supertest';

/**
 * @note Flask app endpoint used only for testing purposes 
 */
const url = 'http://localhost:5000';

describe("GET /course_suggestion - course recommendation endpoint", ()=> {

    it("Should return recommendations list: `Suggestions: [(<title>, <score>)]`", () => {

        let subject = 'Reinforcement Learning';
        let article = 'reinforcement-learning based dialogue system for human-robot interactions with socially-inspired rewards';

        return request(url).get(`/course-suggestion?message=${subject}`)
            .expect(200)
            .expect(response => {
                let answer = JSON.parse(response.text);
                /**
                 * Principal recommendation title
                 */
                let title = answer.suggestions[0][0];
                expect(title).to.be.equal(article);
        });
    });
});
