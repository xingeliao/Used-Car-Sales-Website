import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  userRole: string;

  constructor(
    private http: HttpClient,
    public cookie: CookieService,
    private router: Router,
  ) {

    this.userRole = this.cookie.get('user_role');

  }

  ngOnInit() {}

  logoutUser() {
    location.reload()
    this.cookie.deleteAll('user_role')
    this.cookie.deleteAll('username')
    this.cookie.deleteAll('username-localhost-8888')
    this.router.navigate(['search'])
  }
  
  loginUser() {
    this.router.navigate(['login'])
  }

  navigateToSearch() {
    this.router.navigate(['search'])
  }
}
