import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/service/auth.service';
import { FlashMessageService } from 'src/app/service/flash-messages.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {

  constructor(
    private flashMessage: FlashMessageService,
    private authService: AuthService,
    private router: Router,
  ) { }

  username: String | undefined;
  password: String | undefined;

  onLoginSubmit() {
    const user = {
      username: this.username,
      password: this.password
    }

    this.authService.authenticateUser(user).subscribe({
      next: data => {
        if (data.success) {
          this.authService.storeUserData(data.token, data.user);
          this.flashMessage.show('Erfolgreich angemeldet', { cssClass: 'alert-success', timeout: 5000 });
          this.router.navigate(['/home']);
        } else {
          this.flashMessage.show('Fehler bei der Anmeldung', { cssClass: 'alert-danger', timeout: 5000 });
          this.router.navigate(['/login']);
        }
      },
      error: error => {
        this.flashMessage.show(error, { cssClass: 'alert-danger', timeout: 5000 });
      }
    })
  }
}
