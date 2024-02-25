import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';

export interface FlashMessage {
  text: string;
  cssClass: string;
  timeout: number;
}

@Injectable({
  providedIn: 'root'
})
export class FlashMessageService {
  message = new Subject<FlashMessage>();

  show(text: string, { cssClass, timeout }: { cssClass: string; timeout: number; }) {
    timeout = 50000;
    this.message.next({ text, cssClass, timeout});
  }
}