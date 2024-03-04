import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { AuthService } from './auth.service';
import { environment } from 'src/enviroments/environment';
import { User } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  constructor(
    private http: HttpClient,
    private authService: AuthService,
  ) { }
  
  getUserList(): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });
    
    return this.http.get<any>(
      `${environment.API_URL}/user`, 
      { headers: headers }
    );
  }

  getContributors(): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });
    
    return this.http.get<any>(
      `${environment.API_URL}/user/contributors`, 
      { headers: headers }
    );
  }

  editUser(user_id: string, new_user_obj: User): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });
    
    return this.http.put<any>(
      `${environment.API_URL}/user/${user_id}`, 
      { new_user_obj },
      { headers: headers }
    );
  }

  deleteUser(user_id: string): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });
    
    return this.http.delete<any>(
      `${environment.API_URL}/user/${user_id}`, 
      { headers: headers }
    );
  }
}
