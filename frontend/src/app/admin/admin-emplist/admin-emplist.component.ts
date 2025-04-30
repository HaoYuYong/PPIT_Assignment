import { Component, OnInit } from '@angular/core';
import { IonContent } from '@ionic/angular/standalone';

@Component({
  selector: 'app-admin-emplist',
  templateUrl: './admin-emplist.component.html',
  styleUrls: ['./admin-emplist.component.scss'],
  imports: [IonContent]
})
export class AdminEmplistComponent  implements OnInit {

  constructor() { }

  ngOnInit() {}

}
