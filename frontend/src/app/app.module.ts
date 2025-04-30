import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { IonicModule } from '@ionic/angular';
import { AppComponent } from './app.component';
// import { AppRoutingModule } from './app-routing.module';
import { RouterModule } from '@angular/router';
import { appRoutes } from './app.routes';
// Import your employee components
import { HomeComponent } from './employee/employeehome/employeehome.component';
import { JobseekComponent } from './employee/jobseek/jobseek.component';
import { FavouriteComponent } from './employee/favourite/favourite.component';
import { EmployeeprofileComponent } from './employee/employeeprofile/employeeprofile.component';
import { EmployeefeedbackComponent } from './employee/employeefeedback/employeefeedback.component';
//General
import { HeaderComponent } from './header/header.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { LandingComponent } from './landing/landing.component';
// Import your company components
import { CompanyhomeComponent } from './company/companyhome/companyhome.component';
import { EmpseekComponent } from './company/empseek/empseek.component';
import { EmpfavouriteComponent } from './company/empfavourite/empfavourite.component';
import { CompanyprofileComponent } from './company/companyprofile/companyprofile.component';
import { CompanyfeedbackComponent } from './company/companyfeedback/companyfeedback.component';
// Admin 
import { AdminfeedbacklistComponent } from './admin/adminfeedbacklist/adminfeedbacklist.component';
// Staff
import { StaffquestComponent } from './staff/staffquest/staffquest.component';

// Import Angular Modules
import { FormsModule, ReactiveFormsModule  } from '@angular/forms';

// Import services
import { RegisterService } from './service/register.service';
import { provideHttpClient } from '@angular/common/http';
//HTTP Client
import { HttpClientModule } from '@angular/common/http';


@NgModule({
  declarations: [
    //General
    LandingComponent,
    AppComponent,
    HeaderComponent, 
    LoginComponent,
    RegisterComponent,
    //Employee
    HomeComponent,
    JobseekComponent,
    FavouriteComponent,
    EmployeeprofileComponent,
    EmployeefeedbackComponent,
    //Company
    CompanyhomeComponent,
    EmpseekComponent,
    EmpfavouriteComponent,
    CompanyprofileComponent,
    CompanyfeedbackComponent,
    //Admin
    AdminfeedbacklistComponent,
    //Staff
    StaffquestComponent
  ],
  imports: [
    BrowserModule, 
    IonicModule.forRoot(), 
    RouterModule.forRoot(appRoutes),
    FormsModule, 
    ReactiveFormsModule,
    HttpClientModule
    ],
  schemas: [CUSTOM_ELEMENTS_SCHEMA], // Allow Web Components like <ion-button>
  providers: [RegisterService, provideHttpClient()],
  bootstrap: [AppComponent]
})
export class AppModule {}
