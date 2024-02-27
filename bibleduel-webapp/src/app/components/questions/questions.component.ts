import { Component, OnInit, Input} from '@angular/core';
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
  ) { }

  @Input() categorie_list: any[] = [];
  @Input() question_list: any[] = [];

  ngOnInit() {
  }
}
