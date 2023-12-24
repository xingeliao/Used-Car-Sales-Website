import { AfterViewInit, Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { ApiService } from '../api.service';
import { Location } from '@angular/common';
import { MatTableDataSource } from '@angular/material/table';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-new-vehicle',
  templateUrl: './new-vehicle.component.html',
  styleUrls: ['./new-vehicle.component.scss']
})
export class NewVehicleComponent implements OnInit, AfterViewInit {

  vehicleForm!: FormGroup;

  customerToggle: boolean = false;
  customerSearchForm!: FormGroup;
  customerInvidualForm!: FormGroup;
  customerBusinessForm!: FormGroup;

  purchaseCarForm!: FormGroup;

  // customer table
  displayedColumns: string[] = [];
  dataSource = new MatTableDataSource<any>([]);

  vehicleTypeOptions: string[] = [];
  manufacturerOptions: string[] = [];
  fuelTypeOptions: string[] = []; 
  colorOptions: string[] = [];
  conditionOptions: string[] = [];

  noCustomerFoundMessage = '';
  newCustomerType = 'individual';

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private loc: Location,
    private router: Router,
    private cookie: CookieService
  ) {}

  ngOnInit(): void {
    this.vehicleForm = this.fb.group({
      vehicleType: this.fb.control('', Validators.required),
      manufacturerName: this.fb.control('', Validators.required),
      fuelType: this.fb.control('', Validators.required),
      colors: this.fb.control('', Validators.required),
      modelName: this.fb.control('', Validators.required),
      modelYear: this.fb.control('', Validators.required),
      mileage: this.fb.control('', Validators.required),
      description: this.fb.control(''),
      price: this.fb.control('', Validators.required),
      vin: this.fb.control('', Validators.required),
      condition: this.fb.control('', Validators.required),
      buyingFrom: this.fb.control('', Validators.required)
    });

    this.customerSearchForm = this.fb.group({
      driverLicense: this.fb.control(''),
      taxId: this.fb.control('')
    });

    this.customerInvidualForm = this.fb.group({
      driversLicenseNumber: this.fb.control('', Validators.required),
      firstName: this.fb.control('', Validators.required),
      lastName: this.fb.control('', Validators.required),
      street: this.fb.control('', Validators.required),
      city: this.fb.control('', Validators.required),
      state: this.fb.control('', Validators.required),
      zipCode: this.fb.control('', Validators.required),
      phoneNumber: this.fb.control('', Validators.required),
      email: this.fb.control('')
    });

    this.customerBusinessForm = this.fb.group({
      taxIdNumber: this.fb.control('', Validators.required),
      contactName: this.fb.control('', Validators.required),
      title: this.fb.control('', Validators.required),
      businessName: this.fb.control('', Validators.required),
      street: this.fb.control('', Validators.required),
      city: this.fb.control('', Validators.required),
      state: this.fb.control('', Validators.required),
      zipCode: this.fb.control('', Validators.required),
      phoneNumber: this.fb.control('', Validators.required),
      email: this.fb.control('')
    });

    this.purchaseCarForm = this.fb.group({
      customerID: this.fb.control(''),
      vin: this.fb.control('')
    });

    this.api.getVehicleManufacturers().subscribe({
      next: (res) => {
        const manufacturers = res.data.map((d: any) => d['manufacturer_name']);
        this.manufacturerOptions = manufacturers;
      }
    });

    this.api.getVehicleTypes().subscribe({
      next: (res) => {
        const types = res.data.map((t: any) => t['vehicle_type']);
        this.vehicleTypeOptions = types;
      }
    });

    this.api.getVehicleFuelTypes().subscribe({
      next: (res) => {
        this.fuelTypeOptions = res;
      }
    });

    this.api.getVehicleColors().subscribe({
      next: (res) => {
        const colors = res.data.map((t: any) => t['color']);
        this.colorOptions = colors;
      }
    });

    this.api.getVehicleConditions().subscribe({
      next: (res) => {
        this.conditionOptions = res;
      }
    })
  }

  ngAfterViewInit(): void {
      
  }

  onCustomerToggle(checked: boolean): void {
    this.customerToggle = checked;
  }

  onSave(): void {
    console.log('saving vehicle', this.vehicleForm.value);
    const newVehicle: any = {};
    newVehicle['vin'] = this.vehicleForm.get('vin')?.value;
    newVehicle['vehicle_type'] = this.vehicleForm.get('vehicleType')?.value;
    newVehicle['manufacturer_name'] = this.vehicleForm.get('manufacturerName')?.value;
    newVehicle['fuel_type'] = this.vehicleForm.get('fuelType')?.value;
    newVehicle['colors'] = this.vehicleForm.get('colors')?.value;
    newVehicle['model_name'] = this.vehicleForm.get('modelName')?.value;
    newVehicle['model_year'] = this.vehicleForm.get('modelYear')?.value;
    newVehicle['description'] = this.vehicleForm.get('description')?.value;
    newVehicle['mileage'] = this.vehicleForm.get('mileage')?.value;
    newVehicle['customer_id'] = this.vehicleForm.get('buyingFrom')?.value;
    newVehicle['username'] = this.cookie.get('username');
    newVehicle['purchase_price'] = 100;
    newVehicle['purchase_date'] = new Date().toISOString().split('T')[0];
    newVehicle['vehicle_condition'] = this.vehicleForm.get('condition')?.value;
    
    this.api.addVehicle(newVehicle).subscribe({
      next: (res: any) => {
        alert('vehicle added. click OK to route to detail.');
        this.router.navigate(['/vehicle', res['vin']]);
      }
    });
  }

  onCancel(): void {
    this.vehicleForm.reset();
    this.loc.back();
  }

  searchCustomer(): void {
    const taxId = this.customerSearchForm.get('taxId')?.value;
    const driverLicense = this.customerSearchForm.get('driverLicense')?.value;
    this.noCustomerFoundMessage = "";
    if (taxId && driverLicense) {
      alert('pick either taxId or driverLicense to search for a customer');
      return;
    }
    let id;
    if (taxId) {
      this.api.searchBusinessCustomers(taxId).subscribe(
        (res: any) => {
          if (!res['data'].length) {
            this.noCustomerFoundMessage = 'No Customer found. Add below.';
          }
          this.displayedColumns = ['actions'].concat(res['metadata']);
          this.dataSource.data = res['data'];
        }
      )
    } else if(driverLicense) {
      this.api.searchIndividualCustomers(driverLicense).subscribe(
        (res: any) => {
          if (!res['data'].length) {
            this.noCustomerFoundMessage = 'No Customer found. Add below.';
          }
          this.displayedColumns = ['actions'].concat(res['metadata']);
          this.dataSource.data = res['data'];
        }
      )
      id = driverLicense;
    }
    else{
      alert("Enter either taxId or driverLicense to search for a customer");
    }
  }

  saveCustomer(customerType: string): void {
    if (customerType === 'individual' && this.customerInvidualForm.valid) {
      let new_customer = { 
        "drivers_license_number": this.customerInvidualForm.get('driversLicenseNumber')?.value,
        "street": this.customerInvidualForm.get("street")?.value,
        "city": this.customerInvidualForm.get("city")?.value,
        "state": this.customerInvidualForm.get("state")?.value,
        "postal_code": this.customerInvidualForm.get("zipCode")?.value,
        "phone_number": this.customerInvidualForm.get("phoneNumber")?.value,
        "first_name": this.customerInvidualForm.get("firstName")?.value,
        "last_name": this.customerInvidualForm.get("lastName")?.value,
        "email": this.customerInvidualForm.get("email")?.value 
      };
      this.api.addCustomer(new_customer, null).subscribe(
        (res: any) => {
          this.noCustomerFoundMessage = "";
          this.customerInvidualForm.reset();
          let new_individual: any = res;
          this.customerSearchForm.controls["driverLicense"].setValue(new_individual['driversLicenseNumber'])
          this.customerSearchForm.controls["taxId"].setValue('')
          this.searchCustomer();
        }
        )
      } else if (customerType === 'business' && this.customerBusinessForm.valid) {
      let new_customer = { 
        "tax_id_number": this.customerBusinessForm.get('taxIdNumber')?.value,
        "street": this.customerBusinessForm.get("street")?.value,
        "city": this.customerBusinessForm.get("city")?.value,
        "state": this.customerBusinessForm.get("state")?.value,
        "postal_code": this.customerBusinessForm.get("zipCode")?.value,
        "phone_number": this.customerBusinessForm.get("phoneNumber")?.value,
        "contact_name": this.customerBusinessForm.get("contactName")?.value,
        "title": this.customerBusinessForm.get("title")?.value,
        "email": this.customerBusinessForm.get("email")?.value,
        "business_name": this.customerBusinessForm.get("businessName")?.value 
      };
      this.api.addCustomer(null,new_customer).subscribe(
        (res: any) => {
          this.noCustomerFoundMessage = "";
          this.customerBusinessForm.reset();
          let new_individual: any = res;
          console.log(new_individual)
          this.customerSearchForm.controls["taxId"].setValue(new_individual['taxId'])
          this.customerSearchForm.controls["driverLicense"].setValue('')
          this.searchCustomer();
        }
      )
    } else {
      alert('no a valid customer entry');
      return;
    }
  }

  addCustomerToCarPurchase(customer: any): void {
    console.log('buying car from', customer.customer_id);
    this.vehicleForm.patchValue({
      buyingFrom: customer.customer_id
    });
  }

}
