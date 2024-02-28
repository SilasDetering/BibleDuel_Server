import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';
import { FlashMessageService } from 'src/app/services/flash-messages.service';

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

  username: string | undefined;
  password: string | undefined;

  onLoginSubmit() {
    if(this.username && this.password){
      this.authService.authenticateUser(this.username, this.password).subscribe({
        next: data => {
          this.authService.storeUserData(data.access_token, data.user);
          this.router.navigate(['/dashboard']);
        },
        error: error => {
          this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
        }
      })
    }
  }
}
