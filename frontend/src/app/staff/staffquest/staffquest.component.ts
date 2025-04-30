import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { documentTextOutline } from 'ionicons/icons';

@Component({
  selector: 'app-staffquest',
  templateUrl: './staffquest.component.html',
  styleUrls: ['./staffquest.component.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class StaffquestComponent implements OnInit {
  feedbacks: any[] = [];
  selectedFeedback: any = null;
  replyText: string = '';
  isLoading: boolean = false;
  isSubmitting: boolean = false;
  currentUser: any;

  constructor(private http: HttpClient, private router: Router) {
    addIcons({ documentTextOutline });
  }

  ngOnInit() {
    const userData = sessionStorage.getItem('currentUser');
    if (userData) {
      this.currentUser = JSON.parse(userData);
      this.loadAssignedFeedbacks();
    } else {
      this.router.navigate(['/login']);
    }
  }

  loadAssignedFeedbacks() {
    this.isLoading = true;
    this.http.get(`http://localhost:8000/api/feedback/staff/?staff_id=${this.currentUser.uid}`)
      .subscribe({
        next: (response: any) => {
          this.feedbacks = response;
          this.isLoading = false;
          // Select the first feedback if available
          if (this.feedbacks.length > 0) {
            this.selectFeedback(this.feedbacks[0]);
          }
        },
        error: (error) => {
          console.error('Error loading assigned feedbacks:', error);
          this.isLoading = false;
        }
      });
  }

  selectFeedback(feedback: any) {
    this.selectedFeedback = feedback;
    this.replyText = '';
  }

  submitReply() {
    if (!this.selectedFeedback || !this.replyText) return;

    this.isSubmitting = true;
    
    const payload = {
      bid: this.selectedFeedback.bid,
      reply: this.replyText,
      status: 'resolved'
    };

    this.http.post('http://localhost:8000/api/feedback/reply/', payload)
      .subscribe({
        next: (response: any) => {
          this.isSubmitting = false;
          this.loadAssignedFeedbacks();
          this.replyText = '';
        },
        error: (error) => {
          console.error('Error submitting reply:', error);
          this.isSubmitting = false;
        }
      });
  }
}