export class Report{
    question_id: string;
    reason: string;
    comment: string;
    author: string;

    _toDict(): any {
        return {
            question_id: this.question_id,
            reason: this.reason,
            comment: this.comment,
            author: this.author,
        };
    }
}

export const report_reasons = [
    "Frage oder Antwort ist falsch",
    "Falsche Kategorie",
    "Rechtschreibfeler",
    "Fehlerhafte Quelle",
    "Die Frage existiert bereits",
    "Die Frage ist unverständlich",
    "Die Frage ist irrelevant",
    "Sonstiges"
]