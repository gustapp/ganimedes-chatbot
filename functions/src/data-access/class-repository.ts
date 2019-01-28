import { Repository } from "./repository";
import { ClassProxy } from "../model/business-class";

export class ClasseRepository extends Repository<ClassProxy> {

    constructor(db: FirebaseFirestore.Firestore){
        super(db, 'oferecimentos');
    }

    protected map(data: FirebaseFirestore.DocumentData) : ClassProxy {
        return new ClassProxy(data.codigo_turma, data.tipo_turma);
    }
}
