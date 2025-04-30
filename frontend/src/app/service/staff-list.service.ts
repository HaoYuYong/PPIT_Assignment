import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface User{
  id: number;
  username: string;
  email: string;
  role: string;
}

@Injectable({
  providedIn: 'root'
})
export class StaffListService {

  private apiUrl = 'http://localhost:8000/api/staff-user-list/';

  constructor(private http: HttpClient) { }

  getEmployees(): Observable<User[]>{
    return this.http.get<User[]>(this.apiUrl);
  }
}
