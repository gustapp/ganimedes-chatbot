export abstract class Repository<T> {

    protected readonly collectionRef: FirebaseFirestore.CollectionReference;

    constructor(db: FirebaseFirestore.Firestore, collectionId: string){
        this.collectionRef = db.collection(collectionId); 
    }

    public async get(id?: string) {
        // Get only one entity
        if(id){
            let doc = await this.collectionRef.doc(id).get();
            if (doc.exists) {
                // returns orm data
                return this.map(doc.data());
            } else {
                // no document found
                return undefined;
            }
        }
        // Get collection of documents
        else {
            let querySnapshot = await this.collectionRef.get()
            // Collection of retrieved documents
            let result: T[] = [];
            querySnapshot.forEach(doc => {
                result.push(this.map(doc.data()));
            });
            return result;
        }
    }

    protected abstract map(data: FirebaseFirestore.DocumentData) : T;
}