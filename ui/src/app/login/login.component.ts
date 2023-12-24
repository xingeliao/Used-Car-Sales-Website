import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { FormBuilder, FormGroup } from '@angular/forms';
import { Router } from '@angular/router';
import { CookieService } from 'ngx-cookie-service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent {

  loginForm: FormGroup;
  loginError = '';

  constructor(
    private fb: FormBuilder,
    private http: HttpClient,
    private cookie: CookieService,
    private router: Router
  ) {
    this.loginForm = this.fb.group({
      username: this.fb.control(''),
      password: this.fb.control('')
    });
  }

  login(): void {
    console.log('login info', this.loginForm.value)
    this.http.post('http://localhost:5000/login/', this.loginForm.value).subscribe({
      next: (result: any) => {
        this.loginError = '';
        console.log('logged in successfully', result);
        this.cookie.set('username', result.username);
        this.cookie.set('user_role', result.user_role);

        this.router.navigate(['search']);
      },
      error: (err) => {
        console.error(err);
        this.loginError = 'Incorrect username or password';
      }
    });
  }

}
