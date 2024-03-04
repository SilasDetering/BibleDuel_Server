import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';
import { environment } from 'src/enviroments/environment';


@Injectable({
  providedIn: 'root'
})
export class DuelService {

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }
  
  countDuels(): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });
    
    return this.http.get<any>(
      `${environment.API_URL}/duel/count`, 
      { headers: headers }
    );
  }
}
