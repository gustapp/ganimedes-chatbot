interface IClass {
    code: String;
    type: String;
    getSchedules(): Schedule[];
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

    public getSchedules(): Schedule[] {
        if(!this.class){
            // let daSchedules = new DataAccessSchedules()
            // this.class = 
        }

        return this.class.getSchedules();
    }
}

export class Schedule {
    constructor(readonly weekday: string, readonly start:  string, readonly end: string, readonly teacher: string){}
}

