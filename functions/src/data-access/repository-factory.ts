export class RepositoryFactory {

    constructor(private readonly db){}

    // public static getInstance(db?): RepositoryFactory {
    //     if(!this.instance){
    //         this.instance = new RepositoryFactory(db);
    //     }
    //     return this.instance; 
    // }

    public create<T>(c: {new(db): T; }): T{
        return new c(this.db);
    }
}