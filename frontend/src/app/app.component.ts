import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { HeaderComponent } from './header/header.component'; 
import { LandingComponent } from './landing/landing.component';

@Component({
  selector: 'app-root',
  templateUrl: 'app.component.html',
  styleUrls: ['app.component.scss'],
  standalone: true,
  imports: [CommonModule, RouterModule, IonicModule, HeaderComponent, LandingComponent],
  template: `<app-chat></app-chat>`,
})
export class AppComponent {
  constructor() {}
}
