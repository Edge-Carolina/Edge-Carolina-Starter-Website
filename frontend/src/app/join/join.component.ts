import { Component, OnInit } from "@angular/core";
import { FormBuilder, FormGroup, Validators } from "@angular/forms";

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

  constructor(private fb: FormBuilder) {}

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
      // Here you can handle the form submission, such as sending the data to a server
    }
  }
}
