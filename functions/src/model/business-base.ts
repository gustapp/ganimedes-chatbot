import { DataAccessBase } from "../dao/data-access-base";

export abstract class BusinessBase {

    private dataAccessObject: DataAccessBase<BusinessBase>;

    constructor(db: FirebaseFirestore.Firestore){
        // TODO
    }
}
