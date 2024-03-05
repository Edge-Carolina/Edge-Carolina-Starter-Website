import { Injectable } from "@angular/core";
import {
  Observable,
  OperatorFunction,
  ReplaySubject,
  catchError,
  map,
  throwError,
} from "rxjs";
import { HttpClient } from "@angular/common/http";
import { UserData } from "./userdata";

@Injectable({
  providedIn: "root",
})
export class JoinService {
  private users: ReplaySubject<UserData[]> = new ReplaySubject(1);
  users$: Observable<UserData[]> = this.users.asObservable();

  constructor(protected http: HttpClient) {
    // Sets the initial value of the users replay subject to an empty list of users.
    // This way, we can always guarantee that the next value from `users$` will never be null.
    this.users.next([]);
  }

  /** Refreshes the internal `users$` observable with the latest user data from the API. */
  getUsers() {
    return this.http
      .get<UserData[]>("/api/join")
      .subscribe((timers) => this.users.next(timers));
  }

  /** Returns a single user from the API as an observable.  */
  getUser(id: number): Observable<UserData> {
    return this.http.get<UserData>("/api/join/" + id);
  }

  /** Creates a new user and returns the created user from the API as an observable. */
  createUser(request: UserData): Observable<UserData> {
    return this.http.post<UserData>("/api/join", request).pipe(
      catchError((error) => {
        // Handle specific error status codes or messages as needed
        if (error.status === 405) {
          // Example: Handle UserRegistrationException
          alert("Registration error: email is already registered.");
        }
        // Re-throw the error for further handling if needed
        return throwError(() => new Error("Registration failed"));
      }),
    );
  }

  /** Edits a user and returns the edited user from the API as an observable. */
  editUser(request: UserData): Observable<UserData> {
    return this.http.put<UserData>("/api/join", request);
  }

  /** Deletes a user and returns the delete action as an observable. */
  deleteUser(id: number) {
    return this.http.delete("/api/join/" + id);
  }

  /** Checks if the email is already registered and returns a boolean value as an observable. */
  checkEmailIsRegistered(email: string): Observable<boolean> {
    return this.http.get<boolean>("/api/join", { params: { email } });
  }
}
