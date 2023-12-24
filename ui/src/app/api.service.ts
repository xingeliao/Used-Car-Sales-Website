import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  api = 'http://localhost:5000';

  constructor(
    private http: HttpClient
  ) { }

  getVehicleManufacturers(): Observable<any> {
    const url = `${this.api}/manufacturer/`;
    return this.http.get(url);
  }

  getVehicleVendors(): Observable<any> {
    const url = `${this.api}/vendor/`;
    return this.http.get(url);
  }

  getVehicleTypes(): Observable<any> {
    const url = `${this.api}/vehicle-type/`;
    return this.http.get(url);
  }

  getVehicleFuelTypes(): Observable<any> {
    return of([
      'Battery',
      'Hybrid',
      'Fuel Cell',
      'Gas',
      'Diesel',
      'Natural Gas',
      'Plugin Hybrid'
    ]);
  }

  getVehicleConditions(): Observable<any> {
    return of([
      'Excellent',
      'Very Good',
      'Good',
      'Fair'
    ]);
  }

  getVehicleColors(): Observable<any> {
    const url = `${this.api}/vehicle/color/`;
    return this.http.get(url);
  }

  search_vehicle(params: any): Observable<any> {
    const url = `${this.api}/vehicle`;
    return this.http.get(url, { params });
  }


  search_vehicle_by_vin_manager(params: any): Observable<any> {
    const url = `${this.api}/vehicle/`+ params;
    return this.http.get(url);
  }

  searchCustomer(taxId?: string, dlNum?: string): Observable<any> {
    let url;
    if (taxId) {
      url = `${this.api}/`;
    }
    return of({});
  }

  searchIndividualCustomers(dlNum: string): Observable<any> {
    const url = `${this.api}/customer-individual/search/${dlNum}`;
    return this.http.get(url);
  }
  searchBusinessCustomers(taxId: string): Observable<any> {
    const url = `${this.api}/customer-business/search/${taxId}`;
    return this.http.get(url);
  }

  search_customers(params: any): Observable<any> {
    const url = `${this.api}/customer/search`;
    return this.http.get(url, { params });
  }

  addCustomer(individualCustomer?: any, businessCustomer?: any): Observable<any> | any {
    console.log(individualCustomer)
    console.log(businessCustomer)
    if (individualCustomer) {
      const url = `${this.api}/customer-individual/add`
      return this.http.post(url, individualCustomer)
    } else if (businessCustomer) {
      const url = `${this.api}/customer-business/add`
      return this.http.post(url, businessCustomer)
    } else {
      return null;
    }
  }

  addVehicle(vehicle: any): Observable<any> {
    const url = `${this.api}/vehicle/`;
    return this.http.post(url, vehicle);
  }

  search_vendors(params: any): Observable<any>{
    const url = `${this.api}/vendor`;
    return this.http.get(url, { params });
  }
  
  get_part_orders(params: any): Observable<any> {
    const url = `${this.api}/vehicle/part-order/`+ params;
    return this.http.get(url);
  }

  delete_part_order(params: any): Observable<any>{
    const url = `${this.api}/part/order?purchase_order_number=`+ params;
    return this.http.delete(url);
  }

  get_customer(params: any, type: string): Observable<any>{
    if (type=='individual'){
      const url = `${this.api}/customer-individual/search/` + params;
      return this.http.get(url);
    }
    else{
      const url = `${this.api}/customer-business/search/` + params;
      return this.http.get(url)
    }
  }

  update_part_status(part_id: any, new_status: any): Observable<any> {
    let data = {
      part_id: part_id,
      status: new_status
    }
    const url = `${this.api}/vehicle/update-part-status`;
    return this.http.post(url, data);
  }

  getReport(reportName: string): Observable<any> {
    const url = `${this.api}/report/${reportName}`;
    return this.http.get(url);
  }

  getMonthlyReportDrillDown(params: any): Observable<any> {
    const url = `${this.api}/report/monthly-sales-drilldown`;
    return this.http.get(url, {params});
  }

  managerSearchVehicle(searchType: string): Observable<any> {
    const url = `${this.api}/vehicle?search-type=${searchType}`;
    return this.http.get(url);
  }

}
