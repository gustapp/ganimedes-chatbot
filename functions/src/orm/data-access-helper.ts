export class DataAccessHelper {

    constructor(protected collection: FirebaseFirestore.CollectionReference){}

    listenQuery(returns, options){
        this.collection.onSnapshot(querySnapshot => {
            querySnapshot.forEach(doc => {
                returns(doc.data());
            });
        });
    };

    listenScalar(docId, returns, options){
        this.collection.doc(docId).onSnapshot(doc => {
            returns(doc.data());
        });
    };

    query(returns, errorCallback, options){
        this.collection.get().then(querySnapshot => {
            // Collection of retrieved documents
            querySnapshot.forEach(doc => {
                returns(doc.data());
            });
        }).catch(error => {
            errorCallback(error);
        });
    };

    scalar(docId, returns, emptyCallback, errorCallback){
        this.collection.doc(docId).get().then(doc => {
            if (doc.exists) {
                // returns orm data
                returns(doc.data());
            } else {
                // no document found
                emptyCallback();
            }
        }).catch(error => {
            errorCallback(error);
        });
    };
}