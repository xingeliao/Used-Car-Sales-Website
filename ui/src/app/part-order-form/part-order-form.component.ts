import { Component, Inject } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { ApiService } from '../api.service';
import { MatListOption } from '@angular/material/list';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';

@Component({
  selector: 'app-part-order-form',
  templateUrl: './part-order-form.component.html',
  styleUrls: ['./part-order-form.component.scss']
})
export class PartOrderFormComponent {
  vendorSearchForm: FormGroup;
  addVendorForm: FormGroup;
  addPartOrderForm: FormGroup;
  addPartForm: FormGroup;
  showAddPartFormBool = false;
  partsAdded: Array<any> = []
  partStatus = ['ordered', 'received', 'installed']

  vendorSearchData = []
  showAddVendorFormBool = false

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private cookie: CookieService,
    private router: Router,
    private api: ApiService,
    public dialogRef: MatDialogRef<PartOrderFormComponent>,
    @Inject(MAT_DIALOG_DATA) public diagData: {vin: string},
  ){
    this.addPartOrderForm = this.fb.group({
      part_vendor_name: this.fb.control('', Validators.required),
      total_cost: this.fb.control('', Validators.required)
    })

    this.addPartForm = this.fb.group({
      part_number: this.fb.control('', Validators.required),
      description: this.fb.control('', Validators.required),
      cost: this.fb.control('', Validators.required),
      quantity: this.fb.control('', Validators.required),
      status: this.fb.control('', Validators.required)
    })

    this.vendorSearchForm = this.fb.group({
      name: this.fb.control(''),
      phone: this.fb.control('')
    })

    this.addVendorForm = this.fb.group({
      name: this.fb.control('', Validators.required),
      phonenumber: this.fb.control('', Validators.required),
      street: this.fb.control('', Validators.required),
      city: this.fb.control('', Validators.required),
      state: this.fb.control('', Validators.required),
      postal_code: this.fb.control('', Validators.required)
    })

  }

  searchVendor(): void {
    this.api.search_vendors(this.vendorSearchForm.value).subscribe({
      next: (res) => {
        console.log(res)
        this.vendorSearchData = res['data']

      },
      error: (err) => {
        console.log(err)
      }
    })
  }

  onSelectVendor(options: MatListOption[]): void {
    let selected = options.map(o => o.value)
    console.log('Selected customer', selected)
    this.addPartOrderForm.patchValue({
      part_vendor_name: selected[0].name
    })
    this.vendorSearchData = []
  }

  showAddVendorForm(): void {
    this.showAddVendorFormBool = true
  }

  showAddPartForm(): void {
    this.showAddPartFormBool = true
  }

  saveVendor(): void {
    let data = this.addVendorForm.value
    console.log('vendor data to save', data)
    if (this.addVendorForm.valid){
      this.http.post('http://localhost:5000/vendor/', data).subscribe({
        next: (result: any) => {
          console.log('saved vendor', result)
          this.showAddVendorFormBool = false
          this.addPartOrderForm.patchValue({
            part_vendor_name: result.name
          })
        },
        error: (err) => {
          console.log(err)
        }
      })
    }
    else{
      alert('Please fill required fields')
    }    
  }

  savePart(): void {
    console.log('Save part button', this.addPartForm.value)
    if (this.addPartForm.valid){
      let data: object = this.addPartForm.value
      this.partsAdded.push(data)
      let partsCost: number = this.partsAdded.map(a => a.cost).reduce((acc, val)=> acc+val)
      this.addPartOrderForm.patchValue({
        total_cost: partsCost
      })
      console.log('Array of parts', this.partsAdded)
      this.addPartForm.reset()
    }
    else{
      alert('Please fill required fields')
    }
    
  }

  savePartOrder(): void {
    if (this.addPartOrderForm.valid){
      let body = this.addPartOrderForm.value;
      body['parts'] = this.partsAdded;
      // Add VIN from previous menu selection
      body['vin'] = this.diagData.vin;
      // Add username from session info or cookies
      body['username'] = this.cookie.get('username');
  
      console.log('Request body for add part order', body)
      this.http.post('http://localhost:5000/part/order', body).subscribe({
        next: (result: any) => {
          console.log('saved sale', result);
          alert('Saved');
          this.dialogRef.close();
        },
        error: (err) => {
          console.log(err);
        }
      })
    }
    else{
      alert('Please fill required fields')
    }

  }

}