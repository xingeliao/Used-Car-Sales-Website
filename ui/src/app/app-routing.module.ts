import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { SearchPageComponent } from './search-page/search-page.component';
import { PartOrderFormComponent } from './part-order-form/part-order-form.component';
import { VehicleDetailComponent } from './vehicle-detail/vehicle-detail.component';
import { NewVehicleComponent } from './new-vehicle/new-vehicle.component';
import { ViewPartOrderComponent } from './view-part-order/view-part-order.component';
import { ReportComponent } from './report/report.component';

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'search', component: SearchPageComponent },
  { path: 'partorder', component: PartOrderFormComponent },
  { path: 'vehicle/:vin', component: VehicleDetailComponent },
  { path: 'new-vehicle', component: NewVehicleComponent },
  { path: 'part-order', component: ViewPartOrderComponent },
  { path: 'report/:report-name', component: ReportComponent },
  { path: 'view-part-order/:purchaseOrderNumber', component: ViewPartOrderComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
