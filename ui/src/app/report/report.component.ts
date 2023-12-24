import { AfterViewInit, Component, OnInit, ViewChild, Inject } from '@angular/core';
import { ApiService } from '../api.service';
import { ActivatedRoute } from '@angular/router';
import { MatTableDataSource } from '@angular/material/table';
import { MatPaginator } from '@angular/material/paginator';
import { MatDialogRef, MAT_DIALOG_DATA, MatDialog } from '@angular/material/dialog';

@Component({
  selector: 'app-report',
  templateUrl: './report.component.html',
  styleUrls: ['./report.component.scss']
})
export class ReportComponent implements OnInit, AfterViewInit {

  reportName: string;

  displayedColumns: string[] = [];
  dataSource = new MatTableDataSource<any>([]);

  @ViewChild(MatPaginator) paginator!: MatPaginator;

  constructor(
    private api: ApiService,
    private ar: ActivatedRoute,
    private dialog: MatDialog
  ) {
    this.reportName = this.ar.snapshot.paramMap.get('report-name') || 'seller-history';
  }

  get isMonthlySales(): boolean {
    return this.reportName === 'monthly-sales-summary';
  }
  
  ngOnInit(): void {
    this.api.getReport(this.reportName).subscribe({
      next: (res: any) => {
        console.log(res);
        this.displayedColumns = res['metadata'];
        this.dataSource.data = res['data'];
      },
      error: (err: any) => {
        console.log('error getting report', err);
      }
    });
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
  }

  viewMonthlyReport(row: any): void {
    console.log(row)
    let params = {"month": row['sale_month'], "year": row['sale_year']}
    console.log(params)
    const dialogRef = this.dialog.open(MonthlyDrillDownDialogComponent, {
      data: params
    })
  }

}

@Component({
  selector: 'monthly-drilldown-dialog',
  templateUrl: 'monthly-drill-down.html',
})
export class MonthlyDrillDownDialogComponent {

  month: string;
  year: string;

  dataSource = new MatTableDataSource<any>([]);
  displayedColumns: string[] = [];

  constructor(
    public dialogRef: MatDialogRef<MonthlyDrillDownDialogComponent>,
    private api: ApiService,
    @Inject(MAT_DIALOG_DATA) public params: any
  ) {
    this.month = params['month']
    this.year = params['year']
    this.api.getMonthlyReportDrillDown(params).subscribe(
      (res: any) => {
        console.log(res)
        this.displayedColumns = res['metadata']
        this.dataSource = res['data']
        // console.log("res: " + String(res))
      }
    )
  }
}
