import { Routes } from '@angular/router';
//Employee
import { HomeComponent } from './employee/employeehome/employeehome.component';
import { JobseekComponent } from './employee/jobseek/jobseek.component';
import { FavouriteComponent } from './employee/favourite/favourite.component';
import { EmployeeprofileComponent } from './employee/employeeprofile/employeeprofile.component';
import { EmployeefeedbackComponent } from './employee/employeefeedback/employeefeedback.component';
//Company
import { CompanyhomeComponent } from './company/companyhome/companyhome.component';
import { EmpseekComponent } from './company/empseek/empseek.component';
import { EmpfavouriteComponent } from './company/empfavourite/empfavourite.component';
import { CompanyprofileComponent } from './company/companyprofile/companyprofile.component';
import { ForgotPassComponent } from './forgot-pass/forgot-pass.component';
import { CompanyfeedbackComponent } from './company/companyfeedback/companyfeedback.component';
//General
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { LandingComponent } from './landing/landing.component';
//Staff and Admin
import { AdminStaffListComponent } from './admin/admin-staff-list/admin-stafflist.component';
import { AdminCompanyListComponent } from './admin/admin-company-list/admin-company-list.component';
import { AdminUserListComponent } from './admin/admin-user-list/admin-user-list.component';
import { AdminCreateStaffComponent } from './admin/admin-create-staff/admin-create-staff.component';
import { AdminfeedbacklistComponent } from './admin/adminfeedbacklist/adminfeedbacklist.component';
import { StaffquestComponent } from './staff/staffquest/staffquest.component';
import { StaffUserListComponent } from './staff/staff-user-list/staff-user-list.component';
import { StaffCompanyListComponent } from './staff/staff-company-list/staff-company-list.component';
import { PasswordResetComponent } from './password-reset/password-reset.component';
export const appRoutes: Routes = [
  // Default Route
  { path: '', pathMatch: 'full', redirectTo: 'homepage' },

  //Employee
  { path: 'emp-home', component: HomeComponent },
  { path: 'emp-jobseek', component: JobseekComponent },
  { path: 'emp-favourite', component: FavouriteComponent },
  { path: 'emp-profile', component: EmployeeprofileComponent },
  { path: 'emp-feedback', component: EmployeefeedbackComponent },

  //General
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'homepage', component: LandingComponent },
  { path: 'forgot-password', component: ForgotPassComponent},
  { path: 'password-reset', component: PasswordResetComponent},
  
  //Company
  { path: 'comp-home', component: CompanyhomeComponent },
  { path: 'comp-empseek', component: EmpseekComponent },
  { path: 'comp-profile', component: CompanyprofileComponent },
  { path: 'comp-empfavourite', component: EmpfavouriteComponent},
  { path: 'comp-feedback', component: CompanyfeedbackComponent },

  //Staff and Admin
  { path: 'admin-staff-list', component: AdminStaffListComponent },
  { path: 'admin-companyList', component: AdminCompanyListComponent },
  { path: 'admin-user-list', component: AdminUserListComponent },
  { path: 'admin-create-staff', component: AdminCreateStaffComponent },
  { path: 'admin-feedback', component: AdminfeedbacklistComponent },
  { path: 'staff-quest', component: StaffquestComponent },
  { path: 'staff-user-list', component: StaffUserListComponent },
  { path: 'staff-company-list', component: StaffCompanyListComponent },
];