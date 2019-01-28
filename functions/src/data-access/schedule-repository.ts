import { Repository } from "./repository";
import { Schedule } from "../model/business-class";

export class ScheduleRepository extends Repository<Schedule> {

    constructor(db: FirebaseFirestore.Firestore){
        super(db, 'horarios');
    }

    protected map(data: FirebaseFirestore.DocumentData) : Schedule {
        return new Schedule(data.dia, data.horario_inicio, data.horario_fim, data.professor);
    }
}
