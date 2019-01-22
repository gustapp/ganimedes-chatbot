import { helloWorld } from "../src/index";
import {} from "ts-jest";

import * as chai from "chai";
const expect = chai.expect;

import * as sinon from "ts-sinon";
const stubObject = sinon.stubObject;

interface Test {
    method(): string;
}

describe("HelloWorld function", ()=> {

    it("Should return message `Hello, let's chat!`", () => {

        const req = {
            body: {},
            get: ''
        };

        const res = { 
            send: {
                calledOnce: false,
                firstCall: {
                    args: ''
                }
            } 
        };

        helloWorld(req, res);

        expect(res.send.calledOnce).to.equal(true);
        expect(res.send.firstCall.args).to.be(`Hello, let's chat!`);
    });
})