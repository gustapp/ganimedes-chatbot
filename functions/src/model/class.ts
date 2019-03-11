import { ScheduleRepository } from "../data-access/schedule-repository";
import { RepositoryFactory } from "../data-access/repository-factory";
import { Reference } from "./reference";

interface IClass {
    code: String;
    type: String;
    getSchedules(): Schedule[] | any;
}

export class Class implements IClass {

    constructor(private readonly schedules: Schedule[], readonly code: string, readonly type: string){}

    public getSchedules(): Schedule[]{
        return this.schedules;
    }
}

export class ClassProxy extends Reference implements IClass {
    private class: IClass;

    constructor(docRef: FirebaseFirestore.DocumentReference, readonly code: string, readonly type: string){
        super(docRef);
    }

    public async getSchedules(): Promise<Schedule[]> {
        if(!this.class){
            let daSchedules = this.daHelper
                .create(ScheduleRepository);

            let schedules = await daSchedules.getColl();

            return schedules;
        }

        return this.class.getSchedules();
    }
}

export class Schedule {
    constructor(readonly weekday: string, readonly start:  string, readonly end: string, readonly teacher: string){}
}

