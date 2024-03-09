export class Category {
    constructor(
        public _id: string,
        public title: string,
        public subtitle: string,
        public author: string,
        public color: string,
        public question_count: number,
        public timelimit: number = 20
    ) {}

    static _fromJSON(data: any): Category {
        return new Category(data._id, data.title, data.subtitle, data.author, data.color, data.question_count = 0, data.timelimit? data.timelimit : 20);

    }

    _toDict(): any {
        return {
            _id: this._id,
            title: this.title,
            subtitle: this.subtitle,
            author: this.author,
            color: this.color,
            question_count: this.question_count,
            timelimit: this.timelimit,
        };
    }
}