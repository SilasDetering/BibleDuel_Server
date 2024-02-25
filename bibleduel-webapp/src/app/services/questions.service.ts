import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/enviroments/environment';
import { AuthService } from './auth.service';

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
}
