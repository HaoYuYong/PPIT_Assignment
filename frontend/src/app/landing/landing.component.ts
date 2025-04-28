import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from '../service/landing.service';

@Component({
  selector: 'app-landing',
  templateUrl: './landing.component.html',
  styleUrls: ['./landing.component.scss'],
  imports: [CommonModule, FormsModule],
})
export class LandingComponent{

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