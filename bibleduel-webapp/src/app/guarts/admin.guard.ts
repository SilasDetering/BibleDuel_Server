import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Injectable()
export class AdminGuard implements CanActivate {
    
    constructor(
        private router: Router,
        private authService: AuthService,
    ) { }

    // Prüft für den Zugriff auf gesicherte Seiten ob der Nutzer eingeloggt ist. Falls nicht eingeloggt wird auf die Login Seite umgeleitet 
    canActivate(): boolean {
        if (this.authService.isLoggedIn() && this.authService.getUser()?.role == "admin") {
            return true;
        } else {
            this.router.navigate(['/login']);
            return false;
        }
    }
}