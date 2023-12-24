import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ApiService } from '../api.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatListOption } from '@angular/material/list';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-sell-vehicle-form',
  templateUrl: './sell-vehicle-form.component.html',
  styleUrls: ['./sell-vehicle-form.component.scss'],
})
export class SellVehicleFormComponent {

  addSaleForm: FormGroup;
  customerSearchForm: FormGroup;
  addCustomerForm: FormGroup;
  showAddCustomerFormBool = false;
  showIndividualBool = false;
  showBusinessBool = false;
  customerTypeOptions = ['individual', 'business']

  displayedColumns: string[] = [];
  customerSearchData = []
  customers = []
  selectedCustomer: any = null;

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private cookie: CookieService,
    private router: Router,
    private api: ApiService,
    public dialogRef: MatDialogRef<SellVehicleFormComponent>,
    @Inject(MAT_DIALOG_DATA) public diagData: { vin: string },
  ) {
    this.customerSearchForm = this.fb.group({
      id: this.fb.control('')
    })

    this.addCustomerForm = this.fb.group({
      customer_type: this.fb.control('', Validators.required),
      first_name: this.fb.control('', Validators.required),
      last_name: this.fb.control('', Validators.required),
      street: this.fb.control('', Validators.required),
      city: this.fb.control('', Validators.required),
      state: this.fb.control('', Validators.required),
      postal_code: this.fb.control('', Validators.required),
      phone_number: this.fb.control('', Validators.required),
      drivers_license_number: this.fb.control('', Validators.required),
      contact_name: this.fb.control('', Validators.required),
      title: this.fb.control('', Validators.required),
      tax_id_number: this.fb.control('', Validators.required)
    })

    this.addSaleForm = this.fb.group({
      buyer: this.fb.control('', Validators.required),
      // vin: this.fb.control(''),
      date: this.fb.control('', Validators.required)
    });

  }
  searchCustomer(): void {
    this.api.search_customers(this.customerSearchForm.value).subscribe({
      next: (res) => {
        console.log(res)
        this.displayedColumns = res['metadata']
        this.customerSearchData = res['data']

      },
      error: (err) => {
        console.log(err)
      }
    })
  }

  onSelectCustomer(options: MatListOption[]): void {
    let selected = options.map(o => o.value)
    console.log('Selected customer', selected)
    this.selectedCustomer = selected[0].customer_id
    this.addSaleForm.patchValue({
      buyer: selected[0].id
    })
    this.customerSearchData = []
  }

  checkCustomerExist(id: string): Observable<any> {
    let data = this.addCustomerForm.value
    return this.api.get_customer(id, data.customer_type)

  }

  showAddCustomerForm(): void {
    this.showAddCustomerFormBool = true
  }

  changeCustomerType(): void {
    console.log(this.addCustomerForm.value.customer_type)
    let t = this.addCustomerForm.value.customer_type
    if (t == 'individual') {
      this.showIndividualBool = true
      this.showBusinessBool = false
    } else if (t == 'business') {
      this.showIndividualBool = false
      this.showBusinessBool = true
    }
  }

  saveCustomer(): void {
    const data = this.addCustomerForm.value
    console.log('vendor data to save', data.customer_type)
    let url: string = ''
    let id: string = ''
    if (data.customer_type == 'individual') {
      url = 'http://localhost:5000/customer/add_individual'
      id = data.drivers_license_number
    } else if (data.customer_type == 'business') {
      url = 'http://localhost:5000/customer/add_business'
      id = data.tax_id_number
    }

    if (this.addCustomerForm.valid) {
      // Check for duplicate
      this.checkCustomerExist(id).subscribe((dup: any) => {
        console.log('Duplicates? ', dup)
        if (dup.length > 0) {
          alert('Customer ID already exists')
        }
        else {
          console.log('customer post data', data)
          this.http.post(url, data).subscribe({
            next: (result: any) => {
              console.log('saved customer', result)
              this.showAddCustomerFormBool = false
              this.addSaleForm.patchValue({
                buyer: id
              })
              this.selectedCustomer = result.Customer_Id
              console.log('Select Customer stored ', this.selectedCustomer)
            },
            error: (err) => {
              console.log(err)
            }
          })
        }
      })
    }
    else {
      alert('Please fill required fields')
    }


  }

  saveSale(): void {
    if (!this.addCustomerForm.valid) {
      let data = this.addSaleForm.value
      let username = this.cookie.get('username')
      // VIN selected from inventory page
      let vin = this.diagData.vin
      data['username'] = username
      data['vin'] = vin
      data['customer_id'] = this.selectedCustomer
      data['sale_date'] = data.date
      console.log('customer selected data', data)

      this.http.get('http://localhost:5000/vehicle?vin=' + vin).subscribe({
        next: (result: any) => {
          console.log('get vehicle ' + vin, result)
          data['price'] = result.data.price
        },
        error: (err: any) => {
          console.log(err)
        }
      })

      console.log('save sale', this.addSaleForm.value)
      this.http.post('http://localhost:5000/sale/', data).subscribe({
        next: (result: any) => {
          console.log('saved sale', result)
          alert('Saved')
          this.dialogRef.close();
        },
        error: (err) => {
          console.log(err)
        }
      })
    }
    else {
      alert('Please fill required fields')
    }

  }


}
