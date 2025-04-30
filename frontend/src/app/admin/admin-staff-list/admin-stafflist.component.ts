import { Component, OnInit } from '@angular/core';
import { IonContent, IonGrid, IonRow, IonCol, IonButton } from '@ionic/angular/standalone';
import { StaffListService, User } from 'src/app/service/staff-list.service';
import { CommonModule } from '@angular/common';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-admin-stafflist',
  templateUrl: './admin-stafflist.component.html',
  styleUrls: ['./admin-stafflist.component.scss'],
  imports: [IonContent, IonGrid, IonRow, IonCol, CommonModule, IonButton]
})
export class AdminStaffListComponent  implements OnInit {

  staff: User[] = [];

  constructor(private listService: StaffListService, private alertController: AlertController) { }

  ngOnInit() {
    this.listService.getStaff().subscribe(data=>{
      this.staff = data;
    });
  }

  async confirmDelete(staff: User) {
    const alert = await this.alertController.create({
      header: 'Confirm Delete',
      message: `Are you sure you want to delete ${staff.name}?`,
      buttons: [
        {
          text: 'Delete',
          role: 'destructive',
          handler: () => {
            this.deleteStaff(staff.id);
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

  
  deleteStaff(id: number): void {
    this.listService.deleteStaff(id).subscribe({
      next: () => {
        this.staff = this.staff.filter(e => e.id !== id);
      },
      error: (err) => {
        console.error('Failed to delete staff:', err);
      }
    });
  }
}
