import { Component } from '@angular/core';
import { IonContent, IonButton, IonInput, IonItem, IonLabel } from '@ionic/angular/standalone';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { ResetPasswordService } from '../service/reset-password.service';

@Component({
  selector: 'app-forgot-pass',
  templateUrl: './forgot-pass.component.html',
  styleUrls: ['./forgot-pass.component.scss'],
  standalone: true,
  imports: [IonContent, FormsModule, IonItem, IonButton, IonLabel, IonInput, CommonModule]
})
export class ForgotPassComponent {

  email: string = '';
  message: string = '';
  loading: boolean = false;
  success: boolean = false;
  codeSent: boolean = false;
  codeInput: string = '';
  codeVerified: boolean = false;

  constructor(
    private router: Router,
    private resetpass: ResetPasswordService
  ) {}

  submitForm() {
    if (!this.email.trim()) return;

    this.loading = true;
    this.resetpass.sendResetCode(this.email).subscribe({
      next: () => {
        this.message = 'Code sent to your email.';
        this.success = true;
        this.codeSent = true;
        this.loading = false;
      },
      error: () => {
        this.message = 'Failed to send code.';
        this.success = false;
        this.loading = false;
      }
    });
  }

  verifyCode() {
    if (!this.codeInput.trim()) return;

    this.resetpass.verifyResetCode(this.email, this.codeInput).subscribe({
      next: () => {
        this.message = 'Code verified!';
        this.codeVerified = true;
        this.success = true;
      },
      error: () => {
        this.message = 'Invalid code.';
        this.success = false;
        this.codeVerified = false;
      }
    });
  }

  goToNextPage() {
    localStorage.setItem('reset_email', this.email);
    this.router.navigate(['/password-reset'], { state: { email: this.email } });
  }
}