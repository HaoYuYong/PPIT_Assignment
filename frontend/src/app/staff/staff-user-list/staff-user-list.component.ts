import { Component, OnInit } from '@angular/core';
import { IonContent, IonGrid, IonRow, IonCol, IonButton } from '@ionic/angular/standalone';
import { StaffListService, User } from 'src/app/service/staff-list.service';
import { CommonModule } from '@angular/common';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-staff-user-list',
  templateUrl: './staff-user-list.component.html',
  styleUrls: ['./staff-user-list.component.scss'],
  imports: [IonContent, CommonModule, IonGrid, IonRow, IonCol, IonButton]
})
export class StaffUserListComponent  implements OnInit {

  employees: User[] = [];

  constructor(private listService: StaffListService, private alertController: AlertController) { }

  ngOnInit(){
    this.listService.getEmployees().subscribe((data)=>{
      this.employees = data;
    });
  }

  async confirmDelete(employee: User) {
    const alert = await this.alertController.create({
      header: 'Confirm Delete',
      message: `Are you sure you want to delete ${employee.name}?`,
      buttons: [
        {
          text: 'Delete',
          role: 'destructive',
          handler: () => {
            this.deleteEmployee(employee.id);
          }
        },
        {
          text: 'Cancel',
          role: 'cancel'
        }
      ]
    });
    await alert.present();
  }
  

  deleteEmployee(id: number): void {
    this.listService.deleteEmployee(id).subscribe({
      next: () => {
        this.employees = this.employees.filter(e => e.id !== id);
      },
      error: (err) => {
        console.error('Failed to delete employee:', err);
      }
    });
  }

}


