import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';
import { switchMap } from 'rxjs';
import { PartOrderFormComponent } from '../part-order-form/part-order-form.component';
import { SellVehicleFormComponent } from '../sell-vehicle-form/sell-vehicle-form.component';
import { ApiService } from '../api.service';
import { Router } from '@angular/router';


@Component({
  selector: 'app-vehicle-detail',
  templateUrl: './vehicle-detail.component.html',
  styleUrls: ['./vehicle-detail.component.scss']
})
export class VehicleDetailComponent implements OnInit {

  userRole!: string;
  vin!: string | null;
  vehicle_type!: string ; model_year!: string ; model_name!: string ; mileage!: string ; manufacturer_name!: string ; fuel_type!: string ; color!: string ; description!: string ;
  contact_info!: string ; phone_number!: string ; email!: string ; address!: string ; 
  buyer_contact_info!: string ; buyer_phone_number!: string ; buyer_email!: string ; buyer_address!: string ; 
  clerk_name!: string ; purchase_price!: string ; purchase_date!: string ; 
  salesperson!: string ; sale_date!: string ;
  partOrders!: any;
  total!: number | 0;

  vehicle!: any;

  constructor(
    private ar: ActivatedRoute,
    private cookie: CookieService,
    private dialog: MatDialog,
    private api: ApiService,
    private router: Router
  ) { }

  ngOnInit(): void {
    this.userRole = this.cookie.get('user_role');
    this.vin = this.ar.snapshot.paramMap.get('vin');

    // search vehicle by vin manager role
    this.api.search_vehicle_by_vin_manager(this.vin).subscribe({
      next: (res: any) => {
        console.log('result of search', res);
        this.vehicle_type = res.data.vehicle_type;
        this.model_year = res.data.model_year;
        this.model_name = res.data.model_name;
        this.mileage = res.data.mileage;
        this.manufacturer_name = res.data.manufacturer_name;
        this.fuel_type = res.data.fuel_type;
        this.color = res.data.color;
        this.description = res.data.description;

        this.contact_info = res.data.seller_info?.contact_info;
        this.phone_number = res.data.seller_info?.phone_number;
        this.email = res.data.seller_info?.email;
        this.address = res.data.seller_info?.street + ', ' + res.data.seller_info?.city + ', ' + res.data.seller_info?.state + ', ' + res.data.seller_info.postal_code;
        
        this.clerk_name = res.data.clerk_name;
        this.purchase_price = res.data.purchase_price;
        this.purchase_date = res.data.purchase_date;
        
        this.partOrders = res.data.parts_order;
        this.total = this.partOrders.reduce((total: number, partOrder: any) => total + partOrder.total_cost, 0);

        this.buyer_contact_info = res.data.buyer_info?.contact_info;
        this.buyer_phone_number = res.data.buyer_info?.phone_number;
        this.buyer_email = res.data.buyer_info?.email;
        this.buyer_address = res.data.buyer_info?.street + ', ' + res.data.buyer_info?.city + ', ' + res.data.buyer_info?.state + ', ' + res.data.buyer_info?.postal_code;
        
        this.salesperson = res.data.sale_info?.salesperson;
        this.sale_date = res.data.sale_info?.sale_date;
      }
    })
    // TODO: call to get vehicle detail by vin number
  }
  
  get isPublic(): boolean {
    return !this.userRole;
  }

  get isClerkOrOwner(): boolean {
    return ['InventoryClerk', 'Owner'].includes(this.userRole);
  }

  get isManagerOrOwner(): boolean {
    return ['Manager', 'Owner'].includes(this.userRole);
  }

  get isSalesOrOwner(): boolean {
    return ['SalesPeople', 'Owner'].includes(this.userRole);
  }

  addPartOrder(): void {
    if (!this.isClerkOrOwner) {
      alert('no permission to add part order');
      return;
    }
    const dialogRef = this.dialog.open(PartOrderFormComponent, {
      data: {
        vin: this.vin
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('result of part order dialog', result);
      this.ngOnInit();
    });

  }

  
  deletePartOrder(pon: string): void {
    console.log('Part Order delete param ', pon)
    this.api.delete_part_order(pon).subscribe({
      next: (res)=>{
        console.log('Deleted Part Order', res)
        alert('Deleted :'+ res.purchase_order_number)
        this.ngOnInit();
      },
      error: (err) => {
        console.log('Error deleting part order ', err)
      }
      
    }
    )
  }


















  sellVehicle(): void {
    if (!this.isSalesOrOwner) {
      alert('no permission to sell');
      return;
    }
    const dialogRef = this.dialog.open(SellVehicleFormComponent, {
      data: {
        vin: this.vin
      }
    });

    dialogRef.afterClosed().subscribe(result => {
      console.log('result of sell vehicle dialog', result);
    });
  }

}
