import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/user.model';
import { AuthService } from 'src/app/services/auth.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrl: './dashboard.component.css'
})
export class DashboardComponent implements OnInit {

  constructor(
    private authService: AuthService,
  ) { }

  user: User | undefined;
  
  ngOnInit() {
    this.user = this.authService.getUser();
  }

  changeView(id: string) {
    try {
      document.getElementById("statistics")!.className = "nav-link"
      document.getElementById("tab_statistics")!.className = "tab-pane fade"
      document.getElementById("user")!.className = "nav-link"
      document.getElementById("tab_user")!.className = "tab-pane fade"
      document.getElementById("categories")!.className = "nav-link"
      document.getElementById("tab_categories")!.className = "tab-pane fade"
      document.getElementById("questions")!.className = "nav-link"
      document.getElementById("tab_questions")!.className = "tab-pane fade"

      document.getElementById(id)!.className = "nav-link nav-link active"
      document.getElementById("tab_" + id)!.className = "tab-pane fade active show"
    } catch (error) {
      console.log("Tab-Element konnte nicht gefunden werden")
    }
  }
}
