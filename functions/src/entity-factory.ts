import { object } from "firebase-functions/lib/providers/storage";

/**
 * @class
 * ORM (Object-Relational Mapping) Factory
 * Creates 'Entity' objects
 */
export class EntityFactory {
    /**
     * @constructor
     * @param db 
     */
    constructor(private db: FirebaseFirestore.Firestore){}
    /**
     * @function createRef
     */
    public createRef(collectionName: string){
        return this.db.collection(collectionName);
    }
}
