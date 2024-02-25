import { Component, OnInit } from '@angular/core';
import { User } from 'src/app/models/user.model';
import { FlashMessageService } from 'src/app/services/flash-messages.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrl: './user.component.css'
})
export class UserComponent implements OnInit{

  constructor(
    private userService: UserService,
    private flashMessage: FlashMessageService,
  ) { }

  user_list: User[] = []
  user_delete: User | undefined;

  ngOnInit() {
    this.userService.getUserList().subscribe({
      next: data => {
        this.user_list = data.user_list;
      },
      error: error => {
        this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
      }
    });
  }

  onDelete(user: User) {
    this.user_delete = user;
  }

  onConfirmDelete() {
    console.log("delete")
  }

  onAbort() {
    this.user_delete = undefined;
  }
}
