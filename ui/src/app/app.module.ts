import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { LoginComponent } from './login/login.component';
import { SearchPageComponent } from './search-page/search-page.component';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';
import { MatListModule } from '@angular/material/list';
import {MatDatepickerModule} from '@angular/material/datepicker';
import {MatNativeDateModule} from '@angular/material/core';
import { VehicleDetailComponent } from './vehicle-detail/vehicle-detail.component';
import { NewVehicleComponent } from './new-vehicle/new-vehicle.component';
import { PartOrderFormComponent } from './part-order-form/part-order-form.component';
import { VendorFormComponent } from './vendor-form/vendor-form.component';
import { CustomerFormComponent } from './customer-form/customer-form.component';
import { SellVehicleFormComponent } from './sell-vehicle-form/sell-vehicle-form.component';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatDividerModule } from '@angular/material/divider';
import { MatRadioModule } from '@angular/material/radio';
import { MatToolbarModule } from '@angular/material/toolbar';
import { ViewPartOrderComponent,DialogPartStatus } from './view-part-order/view-part-order.component';
import { MonthlyDrillDownDialogComponent, ReportComponent } from './report/report.component';

@NgModule({
  declarations: [
    AppComponent,
    LoginComponent,
    SearchPageComponent,
    VehicleDetailComponent,
    NewVehicleComponent,
    PartOrderFormComponent,
    VendorFormComponent,
    CustomerFormComponent,
    SellVehicleFormComponent,
    ViewPartOrderComponent,
    MonthlyDrillDownDialogComponent,
    DialogPartStatus,
    ReportComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    CommonModule,
    BrowserModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    MatInputModule,
    MatFormFieldModule, 
    MatButtonModule,
    MatSelectModule,
    MatTableModule,
    MatPaginatorModule,
    MatCardModule,
    MatIconModule,
    MatDialogModule,
    MatCheckboxModule,
    MatDividerModule,
    MatRadioModule,
    MatListModule,
    MatDatepickerModule,
    MatNativeDateModule,
    MatToolbarModule
  ],
  providers: [
    CookieService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
