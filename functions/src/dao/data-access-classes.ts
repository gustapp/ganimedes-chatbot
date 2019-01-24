import { DataAccessBase } from "./data-access-base";
import { ClassProxy } from "../model/business-class";

export class DataAccessClasses extends DataAccessBase<ClassProxy> {

    protected collectionId = 'cursos';

    protected map(data: FirebaseFirestore.DocumentData) : ClassProxy {
        return new ClassProxy(data.codigo_turma, data.tipo_turma);
    }
}
