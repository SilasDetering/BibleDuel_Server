import { Category } from "./category.model";

export class Question {
    _id: string;
    title: string;
    category: Category;
    options: string[];
    answer: string;
    source: string;
    author: string;

    constructor(_id: string, title: string, category: Category, options: string[], answer: string, source?: string, author?: string) {
        this._id = _id;
        this.title = title;
        this.category = category;
        this.options = options;
        this.answer = answer;
        this.source = source || "";
        this.author = author || "unknown";
    }

    _toDict(): any {
        return {
            _id: this._id,
            title: this.title,
            category: this.category._toDict(),
            options: this.options,
            answer: this.answer,
            source: this.source,
            author: this.author
        };
    }

    static _fromJSON(data: any): Question {
        return new Question(
            data._id,
            data.title,
            Category._fromJSON(data.category),
            data.options,
            data.answer,
            data.source,
            data.author
        );
    }
}