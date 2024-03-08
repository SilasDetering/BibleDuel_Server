import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
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
  @Output() refresh = new EventEmitter<boolean>();

  user_selected: User | undefined;
  user_delete: User | undefined;
  filtered_user_list: User[] = [];

  ngOnInit() {
    this.filtered_user_list = this.user_list;
  }

  onSelect(user: User) {
    this.user_selected = Object.assign({}, user);
  }

  searchUser(event: Event): void {
    const searchTerm = (event.target as HTMLInputElement).value;
    this.filtered_user_list = this.user_list.filter(user =>
      user.username.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }

  onFilter(event: Event) {
    const selectedOption = (event.target as HTMLSelectElement).value;
    switch (selectedOption) {
      case 'User':
        this.filtered_user_list = this.user_list.filter(user => user.role === 'user');
        break;
      case 'Admin':
        this.filtered_user_list = this.user_list.filter(user => user.role === 'admin');
        break;
      case 'Mitwirkend':
        this.filtered_user_list = this.user_list.filter(user => user.role === 'contributor');
        break;
      case 'Alle':
      default:
        console.log(this.user_list)
        this.filtered_user_list = this.user_list;
        console.log(this.filtered_user_list)
        break;
    }
  }

  onSave() {
    if (this.user_selected && this.user_selected.username && (this.user_selected.score || this.user_selected.score >= 0) && this.user_selected.role) {

      const new_user_obj = new User(
        this.user_selected._id,
        this.user_selected.username,
        this.user_selected.score,
        this.user_selected.role
      );

      this.userService.editUser(new_user_obj._id, new_user_obj).subscribe({
        next: data => {
          this.flashMessage.show(data.msg, { cssClass: 'alert-success', timeout: 5000 });
          this.refresh.emit(true);
        },
        error: error => {
          this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
        }
      });
    } else {
      this.flashMessage.show('Please fill all fields', { cssClass: 'alert-danger', timeout: 5000 });
    }
  }

  onDelete() {
    if (this.user_delete) {
      this.userService.deleteUser(this.user_delete._id).subscribe({
        next: data => {
          this.flashMessage.show(data.msg, { cssClass: 'alert-success', timeout: 5000 });
          this.refresh.emit(true);
        },
        error: error => {
          this.flashMessage.show(error.message, { cssClass: 'alert-danger', timeout: 5000 });
        }
      });
    }
  }
}
