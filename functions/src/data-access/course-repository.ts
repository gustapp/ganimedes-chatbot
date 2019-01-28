import { Repository } from "./repository";
import { CourseProxy } from "../model/business-course";

export class CourseRepository extends Repository<CourseProxy> {

    constructor(db: FirebaseFirestore.Firestore){
        super(db, 'cursos');
    }

    protected map(data: FirebaseFirestore.DocumentData) : CourseProxy {
        return new CourseProxy(data.sigla, data.name, data.objetivos, data.docentes, data.programa_resumido, data.programa, data.avaliacao, data.bibliografia, data.carga_horaria, data.creditos, data.requisitos);
    }
}
