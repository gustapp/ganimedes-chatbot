from google.cloud.exceptions import NotFound

class FirestoreHelper(object):
    """ Firestore client helper.
    """
    def __init__(self, db):
        self.db = db

    def query(self, coll, filters, ref=False):
        """ Run a simple or compound query, whose operators
            are defined on filters param.
        """
        query_ref = self.db.collection(coll)

        for filter in filters:
            """filter: 3 lenght list
                [<property> <operator> <value>]
            """
            query_ref = query_ref.where(filter[0], filter[1], filter[2])

        docs = query_ref.stream() # run query

        if ref:
            return docs
        else:
            return [x._data for x in docs]

    def get_document(self, coll, id, ref=False):
        """ Retrieve a single document by id.
            Obs: NotFound exception is handled on fault_message.
        """
        doc_ref = self.db.collection(coll).document(id)

        doc = doc_ref.get()

        if not doc.exists:
            raise NotFound('Document {} does not exists'.format(id))

        if ref: # return reference
            return doc
        else: # return data
            return doc._data

    def get_collection(self, coll, ref=False):
        """ Retrieve a collection of documents.
        """
        docs = self.db.collection(coll).stream()
        
        if ref:
            return docs
        else:
            return [x._data for x in docs]