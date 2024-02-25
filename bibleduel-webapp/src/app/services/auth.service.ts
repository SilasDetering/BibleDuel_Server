import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { User } from '../models/user.model';
import { FlashMessageService } from './flash-messages.service';
import { environment } from 'src/enviroments/environment';


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
  authenticateUser(username: string, password: string): Observable<any> {
    let headers = new HttpHeaders();
    headers.append(
      'Content-Type', 'application/json'
    );
    headers.append(
      'App-Version', environment.APP_VERSION
    );
    return this.http.put<any>(
      `${environment.API_URL}/user`,
      { username, password },
      { headers: headers }
    )
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
    if (user) {
      this.user = User._fromJSON(JSON.parse(user));
    }
  }

  getUser() {
    this.loadUser();
    return this.user;
  }

  // Speichert das Anmelde-Token im Local Storage des Clients, damit die Anmeldung nach dem Login verifiziert werden kann.
  storeUserData(token: string, user: any) {
    localStorage.setItem('user', JSON.stringify(user));
    localStorage.setItem('access_token', token);
    this.authToken = token;
    this.user = user;
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
