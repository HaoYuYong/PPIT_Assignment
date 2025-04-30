import { Component, OnInit } from '@angular/core';
import { StaffListService, User } from 'src/app/service/staff-list.service';
import { IonContent, IonGrid, IonRow, IonCol, IonButton} from '@ionic/angular/standalone';
import { CommonModule } from '@angular/common';
import { AlertController } from '@ionic/angular';

@Component({
  selector: 'app-staff-company-list',
  templateUrl: './staff-company-list.component.html',
  styleUrls: ['./staff-company-list.component.scss'],
  imports: [IonContent, IonGrid, IonRow, IonCol, CommonModule, IonButton]
})
export class StaffCompanyListComponent  implements OnInit {


  employers: User[] = [];

  constructor(private listService: StaffListService, private alertController: AlertController) { }

  ngOnInit() {
    this.listService.getEmployers().subscribe(data=>{
      this.employers = data;
    });
  }
  async confirmDelete(employer: User) {
    const alert = await this.alertController.create({
      header: 'Confirm Delete',
      message: `Are you sure you want to delete ${employer.name}?`,
      buttons: [
        {
          text: 'Delete',
          role: 'destructive',
          handler: () => {
            this.deleteEmployer(employer.id);
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
  
  deleteEmployer(id: number): void {
    this.listService.deleteEmployer(id).subscribe({
      next: () => {
        this.employers = this.employers.filter(e => e.id !== id);
      },
      error: (err) => {
        console.error('Failed to delete employer:', err);
      }
    });
  }

}
