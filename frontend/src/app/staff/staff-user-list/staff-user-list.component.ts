import { Component, OnInit } from '@angular/core';
import { IonContent } from '@ionic/angular/standalone';
import { StaffListService, User } from 'src/app/service/staff-list.service';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-staff-user-list',
  templateUrl: './staff-user-list.component.html',
  styleUrls: ['./staff-user-list.component.scss'],
  imports: [IonContent, CommonModule]
})
export class StaffUserListComponent  implements OnInit {

  employees: User[] = [];

  constructor(private listService: StaffListService) { }

  ngOnInit(){
    this.listService.getEmployees().subscribe((data)=>{
      this.employees = data;
    });
  }
}
