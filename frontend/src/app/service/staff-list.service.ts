import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

export interface User{
  id: number;
  name: string;
  email: string;
  role: string;
  phone: string;
  address: string;
}

@Injectable({
  providedIn: 'root'
})
export class StaffListService {

  constructor(private http: HttpClient) { }

  getEmployees(): Observable<User[]>{
    return this.http.get<User[]>('http://localhost:8000/api/user-list/');
  }
  getEmployers(): Observable<User[]>{
    return this.http.get<User[]>('http://localhost:8000/api/company-list/');
  }
  getStaff(): Observable<User[]>{
    return this.http.get<User[]>('http://localhost:8000/api/staff-list/');
  }
  deleteEmployee(id: number): Observable<any> {
    return this.http.delete(`http://localhost:8000/api/employee/${id}/delete/`);
  }
  deleteEmployer(id: number): Observable<any> {
    return this.http.delete(`http://localhost:8000/api/employer/${id}/delete/`);
  }
  deleteStaff(id: number): Observable<any> {
    return this.http.delete(`http://localhost:8000/api/staff/${id}/delete/`);
  }
}
