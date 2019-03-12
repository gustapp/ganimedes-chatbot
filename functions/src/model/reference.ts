import { RepositoryFactory } from "../data-access/repository-factory";

export abstract class Reference {
    protected daHelper: RepositoryFactory;

    constructor(docReference: FirebaseFirestore.DocumentReference) {
        this.daHelper = new RepositoryFactory(docReference);
    }
}