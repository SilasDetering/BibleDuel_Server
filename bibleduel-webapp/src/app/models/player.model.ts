export class Player {
    constructor(
        public _id: string,
        public username: string,
        public score: number,
        public ratio: number[]
    ) { }

    static _fromJSON(json: any): Player {
        const { _id, username, score, ratio } = json;
        return new Player(_id, username, score, ratio);
    }

    _toDict(): any {
        return {
            _id: this._id,
            username: this.username,
            score: this.score,
            ratio: this.ratio
        };
    }
}