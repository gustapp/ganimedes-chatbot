import { DataAccessBase } from "./data-access-base";
import { CourseProxy } from "../model/business-course";

export class DataAccessCourse extends DataAccessBase<CourseProxy> {

    protected collectionId = 'cursos';

    protected map(data: FirebaseFirestore.DocumentData) : CourseProxy {
        return new CourseProxy(data.sigla, data.name, data.objetivos, data.docentes, data.programa_resumido, data.programa, data.avaliacao, data.bibliografia, data.carga_horaria, data.creditos, data.requisitos);
    }
}
