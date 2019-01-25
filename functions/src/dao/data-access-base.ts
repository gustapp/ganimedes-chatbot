export abstract class DataAccessBase<T> {

    protected abstract collectionId;

    constructor(private db: FirebaseFirestore.Firestore){}

    public get(id?: string) {
        // Get only one entity
        if(id){
            return this.db.collection(this.collectionId).doc(id).get().then(doc => {
                if (doc.exists) {
                    // returns orm data
                    return this.map(doc.data());
                } else {
                    // no document found
                    return undefined;
                }
            }).catch(error => {
                return error;
            });
        }
        // Get collection of documents
        else {
            return this.db.collection(this.collectionId).get().then(querySnapshot => {
                // Collection of retrieved documents
                let result = [];
                querySnapshot.forEach(doc => {
                    result.push(this.map(doc.data()));
                });
                return result;
    
            }).catch(error => {
                return error;
            });
        }
    }

    protected abstract map(data: FirebaseFirestore.DocumentData) : T;
}