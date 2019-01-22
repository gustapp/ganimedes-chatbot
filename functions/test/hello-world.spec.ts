import { helloWorld } from "../src/index";
import {} from "ts-jest";

import * as chai from "chai";
const expect = chai.expect;

import * as request from 'supertest';

const url = 'http://localhost:8010/ganimedes-d9ecd/us-central1';

describe("GET /helloWorld - ping function endpoint", ()=> {

    it("Should return greeting: `Hello! Lets chat!`", () => {

        return request(url).get('/helloWorld')
            .expect(200)
            .expect(response => {
                expect(response.text).to.be.equal(`Hello! Lets chat!`);
        });
    });
});
