import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { documentTextOutline, checkmarkCircleOutline } from 'ionicons/icons';

@Component({
  selector: 'app-adminfeedbacklist',
  templateUrl: './adminfeedbacklist.component.html',
  styleUrls: ['./adminfeedbacklist.component.scss'],
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule]
})
export class AdminfeedbacklistComponent implements OnInit {
  feedbacks: any[] = [];
  selectedFeedback: any = null;
  staffList: any[] = [];
  selectedStaffId: string = '';
  showAssignModal: boolean = false;
  isLoading: boolean = false;

  constructor(private http: HttpClient, private router: Router) {
    addIcons({ documentTextOutline, checkmarkCircleOutline });
  }

  ngOnInit() {
    this.loadFeedbacks();
    this.loadStaffList();
  }

  loadFeedbacks() {
    this.isLoading = true;
    this.http.get('http://localhost:8000/api/feedback/all/').subscribe({
      next: (response: any) => {
        this.feedbacks = response;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Error loading feedbacks:', error);
        this.isLoading = false;
      }
    });
  }

  loadStaffList() {
    this.http.get('http://localhost:8000/api/staff/list/').subscribe({
      next: (response: any) => {
        this.staffList = response;
      },
      error: (error) => {
        console.error('Error loading staff list:', error);
      }
    });
  }

  selectFeedback(feedback: any) {
    this.selectedFeedback = feedback;
  }

  openAssignModal() {
    this.selectedStaffId = '';
    this.showAssignModal = true;
  }

  assignFeedback() {
    if (!this.selectedFeedback || !this.selectedStaffId) return;

    this.isLoading = true;
    
    const payload = {
      bid: this.selectedFeedback.bid,
      staff_id: this.selectedStaffId
    };

    this.http.post('http://localhost:8000/api/feedback/assign/', payload)
      .subscribe({
        next: (response: any) => {
          this.isLoading = false;
          this.showAssignModal = false;
          this.loadFeedbacks();
          this.selectedFeedback = response; // Update the selected feedback with new data
        },
        error: (error) => {
          console.error('Error assigning feedback:', error);
          this.isLoading = false;
        }
      });
  }
}