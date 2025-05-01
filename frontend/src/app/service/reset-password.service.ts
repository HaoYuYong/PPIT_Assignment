import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ResetPasswordService {

  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) {}

  sendResetCode(email: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/forgot-password/`, { email });
  }

  verifyResetCode(email: string, code: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/verify-code/`, { email, code });
  }

  resetPassword(email: string, newPassword: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/reset-password/`, {email, new_password: newPassword});
  }

}