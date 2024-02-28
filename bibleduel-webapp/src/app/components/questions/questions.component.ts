import { Component, OnInit, Input, EventEmitter, Output } from '@angular/core';
import { Category } from 'src/app/models/category.model';
import { Question } from 'src/app/models/question.model';
import { CategorieService } from 'src/app/services/categorie.service';
import { FlashMessageService } from 'src/app/services/flash-messages.service';
import { QuestionsService } from 'src/app/services/questions.service';

@Component({
  selector: 'app-questions',
  templateUrl: './questions.component.html',
  styleUrl: './questions.component.css'
})
export class QuestionsComponent implements OnInit {

  constructor(
    private flashMessage: FlashMessageService,
    private questionsService: QuestionsService,
  ) { }

  @Input() categorie_list: any[] = [];
  @Input() question_list: any[] = [];
  @Input() user_list: any[] = [];
  @Output() refresh = new EventEmitter<boolean>();

  selected_question: Question | undefined;

  new_question = {
    title: null,
    category: null,
    opt1: null,
    opt2: null,
    opt3: null,
    opt4: null,
    src: null,
  }

  ngOnInit() { }

  onSelect(question: Question) {
    this.selected_question = Object.assign({}, question);
  }

  getAuthor(author_id: string) {
    const author = this.user_list.find(u => u._id == author_id);
    return author ? author.username : "unknown";
  }

  onSaveNewQuestion() {
    if (!(this.new_question.title == null || this.new_question.category == null || this.new_question.opt1 == null ||
      this.new_question.opt2 == null || this.new_question.opt3 == null || this.new_question.opt4 == null)) {

      const category = this.categorie_list.find(c => c.title == this.new_question.category);
      if (!category) {
        this.flashMessage.show('Category not found', { cssClass: 'alert-danger', timeout: 5000 });
      }

      const question = new Question("0", this.new_question.title, category, [this.new_question.opt1, this.new_question.opt2, this.new_question.opt3, this.new_question.opt4], this.new_question.opt1, this.new_question.src? this.new_question.src: "", "unknown");

      this.questionsService.addQuestion(question).subscribe({
        next: data => {
          this.flashMessage.show('Question added', { cssClass: 'alert-success', timeout: 5000 });
          this.refresh.emit(true);
          this.new_question = {
            title: null,
            category: null,
            opt1: null,
            opt2: null,
            opt3: null,
            opt4: null,
            src: null,
          };
        },
        error: error => {
          this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
        }
      });
    } else {
      this.flashMessage.show('Please fill all fields', { cssClass: 'alert-danger', timeout: 5000 });
    }
  }

  onDeleteQuestion(question: Question) { 
    this.questionsService.deleteQuestion(question._id).subscribe({
      next: data => {
        this.flashMessage.show('Question deleted', { cssClass: 'alert-success', timeout: 5000 });
        this.refresh.emit(true);
        this.selected_question = undefined;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }

  onSaveEditQuestion() {

    if(this.selected_question){
      this.selected_question.category = this.categorie_list.find(c => c.title == this.selected_question?.category);

      this.questionsService.updateQuestion(this.selected_question).subscribe({
        next: data => {
          this.flashMessage.show('Question updated', { cssClass: 'alert-success', timeout: 5000 });
          this.refresh.emit(true);
          this.selected_question = undefined;
        },
        error: error => {
          this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
        }
      });
    }
  }
}
