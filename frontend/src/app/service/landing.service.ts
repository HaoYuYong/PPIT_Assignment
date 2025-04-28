import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({ providedIn: 'root' })
export class ChatService {
  private apiUrl = 'http://localhost:8000/api/chat/';

  constructor(private http: HttpClient) {}

  sendMessage(message: string) {
    return this.http.post<{ reply: string }>(this.apiUrl, { message });
  }
}