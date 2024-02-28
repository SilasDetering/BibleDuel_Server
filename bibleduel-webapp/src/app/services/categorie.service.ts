import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { environment } from 'src/enviroments/environment';
import { AuthService } from './auth.service';
import { Category } from '../models/category.model';

@Injectable({
  providedIn: 'root'
})
export class CategorieService {

  constructor(
    private authService: AuthService,
    private http: HttpClient,
  ) { }

  getCategorieList(): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });
    
    return this.http.get<any>(
      `${environment.API_URL}/categories`, 
      { headers: headers }
    );
  }

  deleteCategorie(id: string): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });

    return this.http.delete<any>(
      `${environment.API_URL}/api/categories/${id}`,
      { headers: headers }
    );
  }

  newCategorie(categorie: Category): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });

    return this.http.post<any>(
      `${environment.API_URL}/api/categories`,
      categorie,
      { headers: headers }
    );
  }

  editCategorie(categorie: Category): Observable<any> {
    this.authService.loadToken();
    let headers = new HttpHeaders({
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + this.authService.authToken
    });

    return this.http.put<any>(
      `${environment.API_URL}/api/categories/${categorie._id}`,
      categorie,
      { headers: headers }
    );
  }
}
