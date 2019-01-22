import { dialogflowFirebaseFulfillment } from "../src/index";
import {} from "ts-jest";

import * as chai from "chai";
const expect = chai.expect;

import * as request from 'supertest';

const url = 'http://localhost:8010/ganimedes-d9ecd/us-central1';

describe("POST /dialogflowFirebaseFulfillment - fulfillment function endpoint", ()=> {

    /**
     * @user Oi
     * @ganimedes Hello! Lets chat 🔥
     */
    it("Welcome: Should return greeting: `Hello! Lets chat 🔥`", () => {

        const welcomeReq = require('./mock/welcome.json');

        return request(url).post('/dialogflowFirebaseFulfillment')
            .send(welcomeReq)
            .expect(200)
            .expect(response => {
                expect(response.text)
                    .to.be.equal(`{"fulfillmentText":"Hello! Lets chat 🔥","outputContexts":[]}`);
        });
    });

    /**
     * @user MAT3458 eh interessante?
     * @ganimedes A disciplina MAT3458 - Álgebra Linear II possui a seguinte descrição: ...
     */
    it("GetCourseInfo: Should return course description for course", () => {

        const getCourseInfoReq = require('./mock/getCourseInfo.json');

        return request(url).post('/dialogflowFirebaseFulfillment')
            .send(getCourseInfoReq)
            .expect(200)
            .expect(response => {
                expect(response.text)
                    .to.be.equal(`{"fulfillmentText":"A disciplina MAT3458 - Álgebra Linear II possui a seguinte descrição: Espaços vetoriais com produto interno, transformações lineares, autovalores e autovetores e diagonalização de operadores lineares. Mostrar como os métodos destes tópicos da Álgebra Linear são importantes para a área de engenharia, com aplicações interessantes e motivadoras.","outputContexts":[]}`);
        });
    });

    /**
     * @user MAT3458 tem quantos creditos?
     * @ganimedes São 4 créditos aula e 0 créditos trabalho
     */
    it("GetCourseCredit: Should return course credits for course", () => {

        const getCourseCreditReq = require('./mock/getCourseCredit.json');

        return request(url).post('/dialogflowFirebaseFulfillment')
            .send(getCourseCreditReq)
            .expect(200)
            .expect(response => {
                expect(response.text)
                    .to.be.equal(`{"fulfillmentText":"São 4 créditos aula e 0 créditos trabalho","outputContexts":[]}`);
        });
    });

    /**
     * @user Quais os requisitos de MAT3458?
     * @ganimedes A disciplina não possui requisitos!
     */
    it("GetCourseRequirements: Should return no requirements for course", () => {

        const getCourseRequirementsReq = require('./mock/getCourseRequirements-empty.json');

        return request(url).post('/dialogflowFirebaseFulfillment')
            .send(getCourseRequirementsReq)
            .expect(200)
            .expect(response => {
                expect(response.text)
                    .to.be.equal(`{"fulfillmentText":"A disciplina não possui requisitos!","outputContexts":[]}`);
        });
    });

    /**
     * @user Qual a carga de MAT3458?
     * @ganimedes A disciplina possui 60 horas por semestre!
     */
    it("GetCourseWorkload: Should return workload for course", () => {

        const getCourseWorkloadReq = require('./mock/getCourseWorkload.json');

        return request(url).post('/dialogflowFirebaseFulfillment')
            .send(getCourseWorkloadReq)
            .expect(200)
            .expect(response => {
                expect(response.text)
                    .to.be.equal(`{"fulfillmentText":"A disciplina possui 60 horas por semestre!","outputContexts":[]}`);
        });
    });

    /**
     * @user Qual o professor de MAT3458? 
     * @ganimedes A disciplina não possui nenhum professor cadastrado no sistema!
     */
    it("GetCourseTeacher: Should return teachers for course", () => {

        const getCourseTeacherReq = require('./mock/getCourseTeacher-empty.json');

        return request(url).post('/dialogflowFirebaseFulfillment')
            .send(getCourseTeacherReq)
            .expect(200)
            .expect(response => {
                expect(response.text)
                    .to.be.equal(`{"fulfillmentText":"A disciplina não possui nenhum professor cadastrado no sistema!","outputContexts":[]}`);
        });
    });

    /**
     * @user  Quais os horarios de MAT3457?
     * @ganimedes A disciplina não possui nenhum professor cadastrado no sistema!
     */
    it("GetCourseSchedule: Should return schedules for course", () => {

        const getCourseScheduleReq = require('./mock/getCourseSchedule.json');

        return request(url).post('/dialogflowFirebaseFulfillment')
            .send(getCourseScheduleReq)
            .expect(200)
            .expect(response => {
                expect(response.text)
                    .to.be.equal(`{"fulfillmentText":"A turma 01 tem horário seg às 09:20 - 11:00 qua às 07:30 - 09:10 . A turma 02 tem horário qua às 15:00 - 16:40 sex às 07:30 - 09:10 . A turma 03 tem horário qua às 13:10 - 14:50 sex às 09:20 - 11:00 . A turma 04 tem horário qua às 09:20 - 11:00 sex às 07:30 - 09:10 . A turma 05 tem horário qua às 07:30 - 09:10 sex às 09:20 - 11:00 . A turma 06 tem horário seg às 07:30 - 09:10 qua às 09:20 - 11:00 . A turma 07 tem horário seg às 13:10 - 14:50 qui às 07:30 - 09:10 . A turma 08 tem horário seg às 09:20 - 11:00 qua às 15:00 - 16:40 . A turma 09 tem horário seg às 07:30 - 09:10 qua às 13:10 - 14:50 . A turma 10 tem horário seg às 09:20 - 11:00 qua às 07:30 - 09:10 . A turma 11 tem horário seg às 07:30 - 09:10 qua às 09:20 - 11:00 . A turma 12 tem horário seg às 15:00 - 16:40 qui às 09:20 - 11:00 . A turma 20 tem horário sex às 08:20 - 11:50 . ","outputContexts":[]}`);
        });
    });

});
