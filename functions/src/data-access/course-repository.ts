import { Repository } from "./repository";
import { CourseProxy } from "../model/course";

export class CourseRepository extends Repository<CourseProxy> {

    constructor(db: FirebaseFirestore.Firestore){
        super(db, 'cursos');
    }

    protected map(data: FirebaseFirestore.DocumentData, ref: FirebaseFirestore.DocumentReference) : CourseProxy {
        return new CourseProxy(ref, data.sigla, data.name, data.objetivos, data.docentes, data.programa_resumido, data.programa, data.avaliacao, data.bibliografia, data.carga_horaria, data.creditos, data.requisitos);
    }
}
