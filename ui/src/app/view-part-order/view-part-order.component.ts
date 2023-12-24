import { Component, Inject } from '@angular/core';
import { MatTableDataSource } from '@angular/material/table';
import { ApiService } from '../api.service';
import {
  MatDialog,
  MatDialogRef,
  MAT_DIALOG_DATA
} from '@angular/material/dialog';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-view-part-order',
  templateUrl: './view-part-order.component.html',
  styleUrls: ['./view-part-order.component.scss']
})
export class ViewPartOrderComponent {

  purchaseOrderNumber!: string | null;
  displayedColumns: any[] = [];
  dataSource = new MatTableDataSource<any>([]);
  newStatus!: string | null;
  partNumber!: string | null;

  constructor(
    private api: ApiService,
    private dialog: MatDialog,
    private route: ActivatedRoute
  ) {
  }

  ngOnInit(): void {
    this.purchaseOrderNumber = this.route.snapshot.paramMap.get('purchaseOrderNumber');
    this.route.paramMap.subscribe(params => {const purchaseOrderNumber = params.get('purchaseOrderNumber');
    this.api.get_part_orders(this.purchaseOrderNumber).subscribe({
      next: (res) => {
        this.dataSource.data = res.data;
        this.displayedColumns = res['metadata'];
      }
    });
  })

}
  

  openDialog(part_num: any, currentStatus: any): void {
    const dialogRef = this.dialog.open(DialogPartStatus, {
      data: { current_status: currentStatus }
    });

    dialogRef.afterClosed().subscribe(result => {

      this.newStatus = result;
      this.partNumber = part_num;
      this.api.update_part_status(this.partNumber, this.newStatus).subscribe({
        next: (res) => {
          console.log("res", res);
          window.location.reload();
        }
      });
    });

  }

}

@Component({
  selector: 'dialog-overview-example-dialog',
  templateUrl: 'dialog-part-status.html',
})
export class DialogPartStatus {

  selected!: string | null;
  partStatusTypeOptions = ["ordered", "received", "installed"];
  current_status!: string | null;

  constructor(
    public dialogRef: MatDialogRef<DialogPartStatus>,
    @Inject(MAT_DIALOG_DATA) public data: { selected: string, current_status: string },
  ) {
    this.current_status = data.current_status
  }


  isOptionDisabled(option: string): boolean {
    if (this.current_status === 'installed' && (option === 'ordered' || option === 'received')) {
      return true;
    } else if (this.current_status === 'received' && option === 'ordered') {
      return true;
    } else {
      return false;
    }
  }
  
  onNoClick(): void {
    this.dialogRef.close(this.selected);
  }
}