import { ApiServiceService } from './../../services/api/api-service.service';
import { Component, OnInit } from '@angular/core';
@Component({
  selector: 'app-login',
  templateUrl: './login.page.html',
  styleUrls: ['./login.page.scss'],
})
export class LoginPage implements OnInit {

    constructor(private api:ApiServiceService) { }
    user: any = {};
    ngOnInit() {
        this.user = {
            loader: false,
            data: {
                email: '',
                password: '',
            }
        }
    }
    login() {
        //console.log(this.user);
        this.user.loader = true;
        this.api.post("/auth", this.user.data).subscribe((res: any) => {
            this.user.loader = false;
            alert("1");
            console.log(res);
        });
    }

}
