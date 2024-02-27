export class User {
    
    constructor(
        public _id: string,
        public username: string,
        public score: number,
        public role: string
    ) {}

    static _fromJSON(json: any): User {
        return new User(
            json._id,
            json.username,
            json.score,
            json.role
        );
    }
}
