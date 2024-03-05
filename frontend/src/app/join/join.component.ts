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
  isEmailRegistered: boolean = false;

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

    this.joinForm.get("email")?.valueChanges.subscribe((value) => {
      this.checkEmailIsRegistered(value);
    });
  }

  checkEmailIsRegistered(email: string) {
    this.joinService.checkEmailIsRegistered(email).subscribe((isRegistered) => {
      this.isEmailRegistered = isRegistered;
    });
  }

  onSubmit(): void {
    if (this.joinForm.valid && !this.isEmailRegistered) {
      console.log("Form Submitted:", this.joinForm.value);
      this.joinService
        .createUser({
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
}
