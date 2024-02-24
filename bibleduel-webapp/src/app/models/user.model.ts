import { Player } from "./player.model";

export class User {
    
    constructor(
        public _id: string,
        public username: string,
        public score: number,
        public role: string
    ) {}

    static _fromJSON(json: any): User {
        const { _id, username, friends, score, role } = json;
        const user = new User(
            _id,
            username,
            score,
            role
        );
        return user;
    }
}
