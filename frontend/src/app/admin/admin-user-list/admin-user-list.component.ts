import { Component, OnInit } from '@angular/core';
import { IonContent } from '@ionic/angular/standalone';

@Component({
  selector: 'app-admin-user-list',
  templateUrl: './admin-user-list.component.html',
  styleUrls: ['./admin-user-list.component.scss'],
  imports: [IonContent]
})
export class AdminUserListComponent  implements OnInit {

  constructor() { }

  ngOnInit() {}

}
