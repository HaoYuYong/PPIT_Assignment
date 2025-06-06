import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ChatService } from 'src/app/service/landing.service';
import { IonContent, IonGrid, IonRow, IonCol } from '@ionic/angular/standalone';

@Component({
  selector: 'app-companyhome',
  templateUrl: './companyhome.component.html',
  styleUrls: ['./companyhome.component.scss'],
  imports: [CommonModule, FormsModule, IonContent, IonGrid, IonRow, IonCol]
})
export class CompanyhomeComponent {

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
