import { Component} from '@angular/core';
import { ChatService} from 'src/app/service/landing.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-home',
  templateUrl: './employeehome.component.html',
  styleUrls: ['./employeehome.component.scss'],
  imports:[CommonModule, FormsModule] 
})
export class HomeComponent{

  message = '';
  chatLog: { from: string; text: string }[] = [];

  constructor(private chatService: ChatService) {}

  loading = false;

  send() {
    if (!this.message.trim()) return;

    this.chatLog.push({ from: 'You', text: this.message });
    this.loading = true;

    this.chatService.sendMessage(this.message).subscribe({
      next: (res) => {
        this.chatLog.push({ from: 'Chat-Bot Assistant', text: res.reply });
        this.loading = false;
      },
      error: (err) => {
        this.chatLog.push({ from: 'AI', text: 'Error: ' + err.message });
        this.loading = false;
      }
    });

    this.message = '';
  }
}