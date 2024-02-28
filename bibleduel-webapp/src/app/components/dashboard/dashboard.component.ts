import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/user.model';
import { AuthService } from 'src/app/services/auth.service';
import { CategorieService } from 'src/app/services/categorie.service';
import { DuelService } from 'src/app/services/duel.service';
import { FlashMessageService } from 'src/app/services/flash-messages.service';
import { QuestionsService } from 'src/app/services/questions.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {

  constructor(
    private authService: AuthService,
    private userService: UserService,
    private flashMessage: FlashMessageService,
    private categorieService: CategorieService,
    private duelService: DuelService,
    private questionService: QuestionsService,
  ) { }

  user: User | undefined;

  user_list: User[] = [];
  question_list: any[] = [];
  categorie_list: any[] = [];
  contributor_list: any[] = [];
  reported_questions: any[] = [];
  duel_count: number = 0;
  
  ngOnInit() {
    this.user = this.authService.getUser();

    this.getUserList();
    this.getCategorieList();
    this.getQuestionList();
    this.getContributors();
    this.getReportedQuestions();
  }

  refresh(event: boolean) {
    if (event) {
      this.getUserList();
      this.getCategorieList();
      this.getQuestionList();
      this.getContributors();
      this.getReportedQuestions();
    }
  }

  loaded() {
    console.log("if loaded")
    return this.user_list.length > 0 && this.question_list.length > 0 && this.categorie_list.length > 0 && this.contributor_list.length > 0 && this.reported_questions.length > 0;
  }

  countDuels(){
    this.duelService.countDuels().subscribe({
      next: data => {
        this.duel_count = data.duel_count;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }

  getUserList() {
    this.userService.getUserList().subscribe({
      next: data => {
        this.user_list = data.user_list;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }

  getQuestionList() {
    this.questionService.getQuestionList().subscribe({
      next: data => {
        this.question_list = data;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }

  getReportedQuestions() {
    this.questionService.getReportedQuestions().subscribe({
      next: data => {
        this.reported_questions = data;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }

  getCategorieList() {
    this.categorieService.getCategorieList().subscribe({
      next: data => {
        this.categorie_list = data.categories;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }

  getContributors() {
    this.userService.getContributors().subscribe({
      next: data => {
        this.contributor_list = data.contributors;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }

  changeView(id: string) {
    try {
      document.getElementById("statistics")!.className = "nav-link"
      document.getElementById("tab_statistics")!.className = "tab-pane fade"
      document.getElementById("user")!.className = "nav-link"
      document.getElementById("tab_user")!.className = "tab-pane fade"
      document.getElementById("categories")!.className = "nav-link"
      document.getElementById("tab_categories")!.className = "tab-pane fade"
      document.getElementById("questions")!.className = "nav-link"
      document.getElementById("tab_questions")!.className = "tab-pane fade"

      document.getElementById(id)!.className = "nav-link nav-link active"
      document.getElementById("tab_" + id)!.className = "tab-pane fade active show"
    } catch (error) {
      console.log("Tab-Element konnte nicht gefunden werden")
    }
  }
}
