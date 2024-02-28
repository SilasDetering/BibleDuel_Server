import { Player } from './player.model';
import { Turn } from './turn.model';

export class Duel {

    public score: Map<string, number>;

    constructor(
        public _id: string,
        public players: Player[],
        public current_player: number,
        public game_state: number,
        public turns: Turn[],
        public current_turn: number,
        public last_edit?: Date,
        public created_at?: Date,
    ) {
        this.created_at = created_at || new Date();
        this.last_edit = last_edit || new Date();
        this.calculateScore();
    }

    getEnemyName(username: string): string {
        return this.players.find(player => player.username !== username).username;
    }

    getIdenx(username: string): number {
        return this.players.findIndex(player => player.username === username);
    }

    getScore(username: string): string {
        this.calculateScore();
        return this.score.get(username) + " : " + this.score.get(this.getEnemyName(username));
    }

    addTurn(turn: Turn) {
        this.turns.push(turn);
    }

    setNextPlayer() {
        if (this.current_player == 0) this.current_player = 1;
        else this.current_player = 0;
    }

    getResult(player_name: string, turn_nr: number, question_nr: number): string {
        const turn = this.turns[turn_nr];

        if (turn == undefined || turn.playerAnswers.get(player_name) == undefined) return "";

        const answer = turn.playerAnswers.get(player_name)[question_nr];

        if(turn.isCorrectAnswer(question_nr, answer)){
            return "✅";
        }else{
            return "❌";
        }
    }

    calculateScore(): Map<string, number> {
        const game_result: Map<string, number> = new Map();

        this.players.forEach(player => {
            game_result.set(player.username, 0);
        });
        
        this.turns.forEach(turn => {
            this.players.forEach(player => {
                const val = turn.getResults(player.username); 
                game_result.set(player.username, game_result.get(player.username) + val);
            });
        });
        
        this.score = game_result;
        return game_result;
    }

    _toDict(): any {
        const players = this.players.map((player: Player) => player._toDict());

        const turns = this.turns.map((turn: Turn) => turn._toDict());

        const dict = {
            _id: this._id,
            players: players,
            current_player: this.current_player,
            game_state: this.game_state,
            turns: turns,
            current_turn: this.current_turn,
            last_edit: this.last_edit,
            created_at: this.created_at
        };
        return dict;
    }

    static _fromJSON(data: any): Duel {
        const players = data.players.map((player: any) => Player._fromJSON(player));
        const turns = data.turns.map((turn: any) => Turn._fromJSON(turn));
        const duel = new Duel(data._id, players, data.current_player, data.game_state, turns, data.current_turn);

        return duel;
    }

    get_player_rank(username: string): number {
        const score = this.score.get(username);
        const enemy_score = this.score.get(this.getEnemyName(username));

        if (score > enemy_score) return 1;
        if (score < enemy_score) return -1;
        return 0;
    }
}