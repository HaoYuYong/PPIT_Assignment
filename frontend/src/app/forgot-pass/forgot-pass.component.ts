import { Component, OnInit } from '@angular/core';
import { IonContent, IonButton, IonInput, IonItem, IonLabel } from '@ionic/angular/standalone';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-forgot-pass',
  templateUrl: './forgot-pass.component.html',
  styleUrls: ['./forgot-pass.component.scss'],
  imports: [IonContent, FormsModule, IonItem, IonButton, IonLabel, IonInput, CommonModule]
})
export class ForgotPassComponent{

  email: string = '';
  message: string = '';
  loading: boolean = false;

  constructor(private http: HttpClient) { }

  submitForm(){
    if(!this.email) return;
    
    this.loading = true;
    this.http.post("http://localhost:8000/api/forgot-password/", { email: this.email})
    .subscribe({
      next: (response: any) => {
        this.message = 'Reset link sent! Check your email.';
        this.loading = false;
      },
      error: (error) => {
        this.message = 'Something went wrong. Please try again.';
        this.loading = false;
      }
    });
  }

}
