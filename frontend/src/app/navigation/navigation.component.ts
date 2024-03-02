import { Component } from "@angular/core";
import { fadeAnimation } from "../animations";

@Component({
  selector: "app-navigation",
  templateUrl: "./navigation.component.html",
  styleUrls: ["./navigation.component.css"],
  animations: [fadeAnimation],
})
export class NavigationComponent {}
