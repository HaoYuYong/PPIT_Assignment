import { Component, OnInit } from '@angular/core';
import { IonContent } from '@ionic/angular/standalone';

@Component({
  selector: 'app-admin-user-feedback',
  templateUrl: './admin-user-feedback.component.html',
  styleUrls: ['./admin-user-feedback.component.scss'],
  imports: [IonContent]
})
export class AdminUserFeedbackComponent  implements OnInit {

  constructor() { }

  ngOnInit() {}

}
