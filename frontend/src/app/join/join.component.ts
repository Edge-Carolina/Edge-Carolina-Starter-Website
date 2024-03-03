import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";
import { JoinService } from "./join.service";
import { UserData } from "./userdata";

@Component({
  selector: "app-join",
  templateUrl: "./join.component.html",
  styleUrls: ["./join.component.css"],
})
export class JoinComponent implements OnInit {
  public static Route = {
    path: "join",
    component: JoinComponent,
  };

  joinForm!: FormGroup;

  constructor(
    private fb: FormBuilder,
    public joinService: JoinService,
  ) {}

  ngOnInit(): void {
    this.joinForm = this.fb.group({
      firstName: ["", Validators.required],
      lastName: ["", Validators.required],
      collegeYear: ["", Validators.required],
      major: ["", Validators.required],
      email: ["", [Validators.required, Validators.email]],
    });
  }

  onSubmit(): void {
    if (this.joinForm.valid) {
      console.log("Form Submitted:", this.joinForm.value);
      this.joinService
        .createUser({
          id: 0,
          first_name: this.joinForm.value.firstName,
          last_name: this.joinForm.value.lastName,
          major: this.joinForm.value.major,
          email: this.joinForm.value.email,
        })
        .subscribe((user: UserData) => {
          alert("User created:");
        });
    }
  }

  getFirstName() {
    this.joinService.getUser(0).subscribe((user: UserData) => {
      alert(user.first_name);
    });
  }
}
