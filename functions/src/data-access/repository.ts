export abstract class Repository<T> {

    protected readonly collectionRef: FirebaseFirestore.CollectionReference;

    constructor(db: FirebaseFirestore.Firestore|FirebaseFirestore.DocumentReference, collectionId: string){
        this.collectionRef = db.collection(collectionId); 
    }

    /**
     * Get the correspondent document 
     * @param id document key
     */
    public async get(id: string) {
        let doc = await this.collectionRef.doc(id).get();
        if (doc.exists) {
            // returns orm data
            return this.map(doc.data(), doc.ref);
        } else {
            // no document found
            return undefined;
        }
    }

    /**
     * @returns Collection of documents
     */
    public async getColl() {
        let querySnapshot = await this.collectionRef.get()
        // Collection of retrieved documents
        let result: T[] = [];
        querySnapshot.forEach(doc => {
            result.push(this.map(doc.data(), doc.ref));
        });
        return result;
    }

    protected abstract map(data: FirebaseFirestore.DocumentData, ref: FirebaseFirestore.DocumentReference) : T;
}