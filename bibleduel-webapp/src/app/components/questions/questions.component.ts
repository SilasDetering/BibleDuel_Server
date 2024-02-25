import { Component, OnInit } from '@angular/core';
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
export class QuestionsComponent implements OnInit{

  constructor(
    private questionService: QuestionsService,
    private categorieService: CategorieService,
    private flashMessage: FlashMessageService,
  ) { }

  categorie_list: Category[] = [];
  question_list: Question[] = [];

  ngOnInit() {
    this.questionService.getQuestionList().subscribe({
      next: data => {
        console.log(data);
        this.question_list = data;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
    this.categorieService.getCategorieList().subscribe({
      next: data => {
        this.categorie_list = data.categories;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }
}
