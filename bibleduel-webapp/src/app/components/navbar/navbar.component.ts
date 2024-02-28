import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  
  constructor(
    private router: Router,
    public authService: AuthService
  ) { }

  navigate(url: string) {
    console.log("click")
    this.router.navigate([url]);
  }
}
