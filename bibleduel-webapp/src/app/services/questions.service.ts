import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/enviroments/environment';
import { AuthService } from './auth.service';
import { Question } from '../models/question.model';

@Injectable({
  providedIn: 'root'
})
export class QuestionsService {

  constructor(
    private authService: AuthService,
    private http: HttpClient,
  ) { }

  getQuestionList(): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });
    
    return this.http.get<any>(
      `${environment.API_URL}/api/questions`, 
      { headers: headers }
    );
  }

  getReportedQuestions(): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });
    
    return this.http.get<any>(
      `${environment.API_URL}/api/questions/report`, 
      { headers: headers }
    );
  }

  addQuestion(question: Question): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });

    return this.http.post<any>(
      `${environment.API_URL}/questions`, 
      { question: question },
      { headers: headers }
    );
  }

  updateQuestion(question: Question): Observable<any> {
    console.log(question);

    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });

    return this.http.put<any>(
      `${environment.API_URL}/api/questions/${question._id}`, 
      { question: question },
      { headers: headers }
    );
  }

  deleteQuestion(question_id: string): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });

    return this.http.delete<any>(
      `${environment.API_URL}/api/questions/${question_id}`, 
      { headers: headers }
    );
  }

  deleteReport(report_id: string): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });

    return this.http.delete<any>(
      `${environment.API_URL}/api/questions/report/${report_id}`, 
      { headers: headers }
    );
  }
}
