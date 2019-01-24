import { DataAccessBase } from "./data-access-base";
import { Schedule } from "../model/business-class";

export class DataAccessSchedules extends DataAccessBase<Schedule> {

    protected collectionId = 'cursos';

    protected map(data: FirebaseFirestore.DocumentData) : Schedule {
        return new Schedule(data.dia, data.horario_inicio, data.horario_fim, data.professor);
    }
}
