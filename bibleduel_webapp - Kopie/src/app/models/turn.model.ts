import { Category } from "./category.model";
import { Question } from "./question.model";

export class Turn {
    questions: Question[];
    category: Category;
    playerAnswers: Map<string, string[]>;  // Playername -> Answers

    constructor(questions: Question[], category: Category, playerAnswers?: Map<string, string[]>) {
        this.questions = questions;
        this.category = category;
        this.playerAnswers = playerAnswers || new Map();
    }

    isCorrectAnswer(question_i: number, answer: string) {
        return this.questions[question_i].answer == answer;
    }

    setPlayerAnswers(player_name: string, answers: string[]) {
        this.playerAnswers.set(player_name, answers);
    }

    getResults(player_name: string): number {
        let rtnvl: number = 0;

        this.playerAnswers.get(player_name)?.forEach((answer, index) => {
            if (this.isCorrectAnswer(index, answer)) {
                rtnvl += 1;
            }
        });

        return rtnvl;
    }

    hasPlayed(player_name: string): boolean {
        return this.playerAnswers.has(player_name);
    }

    _toDict(): any {
        const playerAnswersDict: any = {};
        this.playerAnswers.forEach((answers, player) => {
            playerAnswersDict[player] = answers;
        });
        return {
            questions: this.questions.map(question => question._toDict()),
            category: this.category._toDict(),
            playerAnswers: playerAnswersDict
        };
    }

    static _fromJSON(data: any): Turn {
        const questions = data.questions.map((questionData: any) => Question._fromJSON(questionData));
        const category = Category._fromJSON(data.category);

        const playerAnswersMap = new Map<string, string[]>();
        
        if (data.playerAnswers) {
            Object.keys(data.playerAnswers).forEach((playerKey: string) => {
                const playerAnswers = data.playerAnswers[playerKey];
                playerAnswersMap.set(playerKey, playerAnswers);
            });
        }
        return new Turn(questions, category, playerAnswersMap);
    }
}