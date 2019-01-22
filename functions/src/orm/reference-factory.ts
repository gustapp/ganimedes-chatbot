import { DataAccessHelper } from "./data-access-helper";

/**
 * @class
 * ORM (Object-Relational Mapping) Factory
 * Creates 'Reference' objects
 */
export class ReferenceFactory {
    /**
     * @constructor
     * @param db 
     */
    constructor(private db: FirebaseFirestore.Firestore){}
    /**
     * @function createRef
     */
    public createRef(collectionName: string) : DataAccessHelper{
        return new DataAccessHelper(this.db.collection(collectionName));
    }
}
