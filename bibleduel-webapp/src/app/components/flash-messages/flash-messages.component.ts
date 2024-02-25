import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { FlashMessage, FlashMessageService } from 'src/app/services/flash-messages.service';

@Component({
  selector: 'app-flash-messages',
  templateUrl: './flash-messages.component.html',
  styleUrls: ['./flash-messages.component.css']
})
export class FlashMessagesComponent implements OnInit, OnDestroy {

  constructor(
    private flashMessage: FlashMessageService
  ) { }

  message: FlashMessage | null = null;
  private subscription: Subscription | undefined;

  ngOnInit() {
    this.subscription = this.flashMessage.message.subscribe(msg => {
      this.message = msg;
      if (msg) {
        setTimeout(() => this.message = null, msg.timeout);
      }
    });
  }

  ngOnDestroy() {
    if(this.subscription){
      this.subscription.unsubscribe();
    }
  }
}