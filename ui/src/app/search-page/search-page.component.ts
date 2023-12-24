import { HttpClient } from '@angular/common/http';
import { AfterViewInit, Component, OnInit, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup } from '@angular/forms';
import { CookieService } from 'ngx-cookie-service';
import { ApiService } from '../api.service';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { Router } from '@angular/router';

@Component({
  selector: 'app-search-page',
  templateUrl: './search-page.component.html',
  styleUrls: ['./search-page.component.scss']
})
export class SearchPageComponent implements OnInit, AfterViewInit {

  userRole: string;
  publicSearchForm!: FormGroup;

  manufacturerOptions = [];
  vendorOptions = [];
  vehicleTypeOptions = [];
  fuelTypeOptions = [];
  colorOptions: string[] = [];

  displayedColumns: string[] = [];
  dataSource = new MatTableDataSource<any>([]);

  noVehiclesFoundMessage = "";

  numPendingVehicles = 0;
  numAvailableVehicles = 0;

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private cookie: CookieService,
    private fb: FormBuilder,
    private http: HttpClient,
    private api: ApiService,
    private router: Router
  ) {
    this.userRole = this.cookie.get('user_role');
  }

  get shouldDisplayVin(): boolean {
    return ['Owner', 'SalesPeople', 'InventoryClerk', 'Manager'].includes(this.userRole);
  }

  get shouldDisplayClerkCard(): boolean {
    return ['InventoryClerk', 'Owner'].includes(this.userRole);
  }

  get shouldDisplayMgrCard(): boolean {
    return ['Manager', 'Owner'].includes(this.userRole);
  }

  get shouldDisplaySalespeopleCard(): boolean {
    return ['SalesPeople', 'Owner'].includes(this.userRole);
  }

  ngOnInit(): void {
    this.publicSearchForm = this.fb.group({
      vehicleType: this.fb.control(''),
      manufacturerName: this.fb.control(''),
      fuelType: this.fb.control(''),
      modelName: this.fb.control(''),
      modelYear: this.fb.control(''),
      description: this.fb.control(''),  // keyword
      mileage: this.fb.control(''),
      price: this.fb.control(''),
      vin: this.fb.control(''),
      colors: this.fb.control('')
    });

    this.api.getVehicleManufacturers().subscribe({
      next: (res) => {
        console.log(res);
        const manufacturers = res.data.map((d: any) => d['manufacturer_name']);
        this.manufacturerOptions = manufacturers;
      }
    });

    this.api.getVehicleTypes().subscribe({
      next: (res) => {
        console.log(res);
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
    this.api.search_vehicle({}).subscribe({
      next: (res: any) => {
        const allVehicles: [] = res['data'];
        const availableVehicles = allVehicles.filter((v: any) => v.vin_status === 'available');
        const pendingVehicles = allVehicles.filter((v: any) => v.vin_status === 'pending');
        this.numPendingVehicles = pendingVehicles.length;
        this.numAvailableVehicles = availableVehicles.length;
      }
    });
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
  }

  search(): void {
    this.noVehiclesFoundMessage = "";
    const params: any = {};

    const vehicleType = this.publicSearchForm.get('vehicleType')?.value;
    if (vehicleType) {
      params['vehicle-type'] = vehicleType;
    }
    const manufacturerName = this.publicSearchForm.get('manufacturerName')?.value;
    if (manufacturerName) {
      params['manufacturer-name'] = manufacturerName;
    }
    const fuelType = this.publicSearchForm.get('fuelType')?.value;
    if (fuelType) {
      params['fuel-type'] = fuelType;
    }
    const modelName = this.publicSearchForm.get('modelName')?.value;
    if (modelName) {
      params['model-name'] = modelName;
    }
    const modelYear = this.publicSearchForm.get('modelYear')?.value;
    if (modelYear) {
      params['model-year'] = modelYear;
    }
    const description = this.publicSearchForm.get('description')?.value;
    if (description) {
      params['kw'] = description;
    }
    const mileage = this.publicSearchForm.get('mileage')?.value;
    if (mileage) {
      params['mileage'] = mileage;
    }
    const price = this.publicSearchForm.get('price')?.value;
    if (price) {
      params['price'] = price;
    }
    const vin = this.publicSearchForm.get('vin')?.value;
    if (vin) {
      params['vin'] = vin;
    }
    const colors: [] = this.publicSearchForm.get('colors')?.value;
    if (colors) {
      params['colors'] = colors.join(',');
    }
    
    this.api.search_vehicle(params).subscribe({
      next: (res: any) => {
        this.displayedColumns = ['actions'].concat(res['metadata']).filter((column: string) => column !== 'vin_status');
        const allVehicles: [] = res['data'];

        this.noVehiclesFoundMessage = res['data'].length == 0 ? "Sorry! We cannot find the vehicle you are looking for!" : ""
        if (this.shouldDisplayClerkCard) {
          this.dataSource.data = allVehicles;
        } else {
          const availableVehicles = allVehicles.filter((v: any) => v.vin_status === 'available');
          this.dataSource.data = availableVehicles;
        }
      }
    });
  }

  reset(): void {
    this.publicSearchForm.reset();
    this.dataSource.data = [];
    this.noVehiclesFoundMessage = "";
  }

  onAddVehicleClick(): void {
    if (!this.shouldDisplayClerkCard) {
      alert('no permission to navigate');
      return;
    }
    this.router.navigate(['/new-vehicle']);
  }

  managerSearchVehicle(searchType: string): void {
    if (!this.shouldDisplayMgrCard) {
      alert('you cannot see this');
      return;
    }
    if (searchType === 'sold') {
      this.api.managerSearchVehicle('sold').subscribe({
        next: (res: any) => {
          this.dataSource.data = res['data'];
          this.noVehiclesFoundMessage = res['data'].length == 0 ? "Sorry! We cannot find the vehicle you are looking for!" : ""
          this.displayedColumns = ['actions'].concat(res['metadata']).filter((column: string) => column !== 'vin_status');
        }
      });
    } else if (searchType === 'unsold') {
      this.api.managerSearchVehicle('unsold').subscribe({
        next: (res: any) => {
          this.dataSource.data = res['data'];
          this.noVehiclesFoundMessage = res['data'].length == 0 ? "Sorry! We cannot find the vehicle you are looking for!" : ""
          this.displayedColumns = ['actions'].concat(res['metadata']).filter((column: string) => column !== 'vin_status');
        }
      });
    } else if (searchType === 'all') {
      this.api.managerSearchVehicle('all').subscribe({
        next: (res: any) => {
          this.dataSource.data = res['data'];
          this.noVehiclesFoundMessage = res['data'].length == 0 ? "Sorry! We cannot find the vehicle you are looking for!" : ""
          this.displayedColumns = ['actions'].concat(res['metadata']).filter((column: string) => column !== 'vin_status');
        }
      });
    }
  }

}
