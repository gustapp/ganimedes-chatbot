import { Repository } from "./repository";
import { ClassProxy } from "../model/class";

export class ClassRepository extends Repository<ClassProxy> {

    constructor(db: FirebaseFirestore.Firestore){
        super(db, 'oferecimentos');
    }

    protected map(data: FirebaseFirestore.DocumentData, ref: FirebaseFirestore.DocumentReference) : ClassProxy {
        return new ClassProxy(ref, data.codigo_turma, data.tipo_turma);
    }
}
