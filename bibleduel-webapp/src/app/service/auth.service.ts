import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { User } from '../models/user.model';
import { FlashMessageService } from './flash-messages.service';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  constructor(
    private flashMessage: FlashMessageService,
    private http: HttpClient,
  ) { }

  authToken: string | null = null;
  user: User | undefined;

  // Übergibt ein User-Objekt zum authentifizieren an den Server
  authenticateUser(user: { username: String | undefined; password: String | undefined; }): Observable<any> {
    let headers = new HttpHeaders();
    headers.append('Content-Type', 'application/json');
    return this.http.post<any>('/authenticate', user, { headers: headers })
  }

  // Löscht das Anmelde-Token aus dem Local Storage des Clients
  logout() {
    this.authToken = null;
    this.user = undefined;
    localStorage.clear();
  }

  // Läd das Token access_token aus dem Local Storage
  loadToken() {
    const token = localStorage.getItem('access_token');
    this.authToken = token;
  }

  // Läd aktuellen User aus dem Local Storage
  loadUser() {
    const user = localStorage.getItem('user');
    this.user = User._fromJSON(user);
  }

  // Speichert das Anmelde-Token im Local Storage des Clients, damit die Anmeldung nach dem Login verifiziert werden kann.
  storeUserData(token: string, user: any) {
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', token);
    this.authToken = token;
    this.user = user;
  }

  /**
  * Überprüft, ob der Benutzer Admin-Rechte besitzt
  */
  isAdmin() {
    const user = this.loadUser();
    if (this.user) {
      return this.user.role === 'admin';
    }
    return false;
  }

  // Prüft ob das Token im Lokal Storage des Browsers abgelaufen ist
  isLoggedIn() {
    this.loadToken();
    if (this.authToken == null) {
      return false;
    }
    return true;
  }
}
