export class RepositoryFactory {

    private static instance: RepositoryFactory;

    private constructor(private readonly db){}

    public static getInstance(db?): RepositoryFactory {
        if(this.instance){
           return this.instance; 
        }

        return new RepositoryFactory(db);
    }

    public create<T>(c: {new(db): T; }): T{
        return new c(this.db);
    }
}