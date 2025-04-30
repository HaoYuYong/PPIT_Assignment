import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { personCircleOutline } from 'ionicons/icons';

@Component({
  selector: 'app-employeefeedback',
  templateUrl: './employeefeedback.component.html',
  styleUrls: ['./employeefeedback.component.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class EmployeefeedbackComponent implements OnInit {
  feedback = {
    title: '',
    description: ''
  };
  feedbacks: any[] = [];
  isLoading = false;
  currentUser: any;

  constructor(private http: HttpClient, private router: Router) {
    addIcons({ personCircleOutline });
  }

  ngOnInit() {
    const userData = sessionStorage.getItem('currentUser');
    if (userData) {
      this.currentUser = JSON.parse(userData);
      this.loadUserFeedback();
    } else {
      this.router.navigate(['/login']);
    }
  }

  submitFeedback() {
    if (!this.feedback.title || !this.feedback.description) return;
    
    this.isLoading = true;
    
    const payload = {
      uid: this.currentUser.uid,
      f_title: this.feedback.title,
      f_description: this.feedback.description
    };

    this.http.post('http://localhost:8000/api/feedback/submit/', payload)
      .subscribe({
        next: (response: any) => {
          this.isLoading = false;
          this.feedback = { title: '', description: '' };
          this.loadUserFeedback();
        },
        error: (error) => {
          console.error('Error submitting feedback:', error);
          this.isLoading = false;
        }
      });
  }

  loadUserFeedback() {
    this.http.get(`http://localhost:8000/api/feedback/user/?uid=${this.currentUser.uid}`)
      .subscribe({
        next: (response: any) => {
          this.feedbacks = response;
        },
        error: (error) => {
          console.error('Error loading feedback:', error);
        }
      });
  }

  getStatusClass(status: string): string {
    switch (status) {
      case 'new': return 'status-new';
      case 'assigned': return 'status-assigned';
      case 'resolved': return 'status-resolved';
      default: return '';
    }
  }
}