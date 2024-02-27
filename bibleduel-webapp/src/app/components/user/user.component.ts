import { Component, OnInit, Input } from '@angular/core';
import { User } from 'src/app/models/user.model';
import { FlashMessageService } from 'src/app/services/flash-messages.service';
import { UserService } from 'src/app/services/user.service';

@Component({
  selector: 'app-user',
  templateUrl: './user.component.html',
  styleUrl: './user.component.css'
})
export class UserComponent implements OnInit {

  constructor(
    private flashMessage: FlashMessageService,
    private userService: UserService,
  ) { }

  @Input() user_list: User[] = []

  user_selected: User | undefined;
  user_delete: User | undefined;

  ngOnInit() {
  }

  onSave() {
    if (this.user_selected) {

      const new_user_obj = new User(
        this.user_selected._id,
        this.user_selected.username,
        this.user_selected.score,
        this.user_selected.role
      );

      this.userService.editUser(new_user_obj._id, new_user_obj).subscribe({
        next: data => {
          this.flashMessage.show(data.msg, { cssClass: 'alert-success', timeout: 5000 });
        },
        error: error => {
          this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
        }
      });
    }
  }

  onDelete() {
    if (this.user_delete) {
      this.userService.deleteUser(this.user_delete._id).subscribe({
        next: data => {
          this.flashMessage.show(data.msg, { cssClass: 'alert-success', timeout: 5000 });
        },
        error: error => {
          this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
        }
      });
    }
  }
}
