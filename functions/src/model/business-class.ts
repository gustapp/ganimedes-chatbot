import { ScheduleRepository } from "../data-access/schedule-repository";
import { RepositoryFactory } from "../data-access/repository-factory";

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

export class ClassProxy implements IClass {
    private class: IClass;

    constructor(readonly code: string, readonly type: string){}

    public async getSchedules() {
        if(!this.class){
            let repoFactory = RepositoryFactory.getInstance();

            let daSchedules = repoFactory
                .create(ScheduleRepository);

            let schedules = await daSchedules.get();

            return schedules;
        }

        return this.class.getSchedules();
    }
}

export class Schedule {
    constructor(readonly weekday: string, readonly start:  string, readonly end: string, readonly teacher: string){}
}

