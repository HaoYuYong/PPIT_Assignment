import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { IonContent, IonItem, IonLabel, IonInput, IonButton } from '@ionic/angular/standalone';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-password-reset',
  templateUrl: './password-reset.component.html',
  styleUrls: ['./password-reset.component.scss'],
  imports: [IonContent, IonItem, IonLabel, IonInput, CommonModule, FormsModule, IonButton]
})
export class PasswordResetComponent implements OnInit {
  email = '';
  newPassword = '';
  confirmPassword = '';
  message = '';
  success = false;

  constructor(private router: Router, private http: HttpClient) {}

  ngOnInit() {
    const nav = this.router.getCurrentNavigation();
    const emailFromState = nav?.extras?.state?.['email'];

    this.email = emailFromState || localStorage.getItem('reset_email') || '';

    if (!this.email) {
      this.message = 'No email found. Please restart the password reset process.';
    }
  }

  resetPassword() {
    if (this.newPassword !== this.confirmPassword) {
      this.message = 'Passwords do not match.';
      this.success = false;
      return;
    }

    this.http.post('http://localhost:8000/api/reset-password/', {
      email: this.email,
      new_password: this.newPassword
    }).subscribe({
      next: () => {
        this.message = 'Password successfully reset!';
        this.success = true;
        setTimeout(() => this.router.navigate(['/login']), 2000);
      },
      error: () => {
        this.message = 'Failed to reset password.';
        this.success = false;
      }
    });
  }
}