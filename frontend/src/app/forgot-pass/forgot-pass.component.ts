import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonContent, IonButton, IonInput, IonItem, IonLabel } from '@ionic/angular/standalone';

@Component({
  selector: 'app-forgot-pass',
  templateUrl: './forgot-pass.component.html',
  styleUrls: ['./forgot-pass.component.scss'],
  standalone: true,
  imports: [CommonModule, FormsModule, IonContent, IonButton, IonInput, IonItem, IonLabel],
})
export class ForgotPassComponent {
  email: string = '';
  message: string = '';
  loading: boolean = false;
  showProceedButton: boolean = false;

  constructor(private http: HttpClient, private router: Router) {}

  submitForm() {
    if (!this.email) return;
  
    this.loading = true;
    this.message = '';
  
    this.http.post('http://localhost:8000/api/forgot-password/', {
      email: this.email
    }).subscribe({
      next: (response: any) => {
        this.message = 'Check your email.';
        this.loading = false;
        this.showProceedButton = true;
      },
      error: (error) => {
        if (error.error && error.error.error) {
          this.message = error.error.error;
        } else {
          this.message = 'Something went wrong. Please try again.';
        }
        this.loading = false;
      }
    });
  }   

  goToLoginPage() {
    this.router.navigate(['/login'], { queryParams: { email: this.email } });
  }
}