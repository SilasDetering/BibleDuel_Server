export class Category {
    constructor(
        public _id: string,
        public title: string,
        public subtitle: string,
        public author: string,
        public color: string,
    ) {}

    static _fromJSON(data: any): Category {
        return new Category(data._id, data.title, data.subtitle, data.author, data.color);
    }

    _toDict(): any {
        return {
            _id: this._id,
            title: this.title,
            subtitle: this.subtitle,
            author: this.author,
            color: this.color
        };
    }
}