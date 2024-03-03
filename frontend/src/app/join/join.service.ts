import { Injectable } from "@angular/core";
import { Observable, OperatorFunction, ReplaySubject, map } from "rxjs";
import { HttpClient } from "@angular/common/http";
import { UserData } from "./userdata";

@Injectable({
  providedIn: "root",
})
export class JoinService {
  private users: ReplaySubject<UserData[]> = new ReplaySubject(1);
  users$: Observable<UserData[]> = this.users.asObservable();

  constructor(protected http: HttpClient) {
    // Sets the initial value of the timers replay subject to an empty list of timers.
    // This way, we can always guarantee that the next value from `timers$` will never be null.
    this.users.next([]);
  }

  /** Refreshes the internal `timer$` observable with the latest timer data from the API. */
  getTimers() {
    return this.http
      .get<UserData[]>("/api/productivity")
      .subscribe((timers) => this.users.next(timers));
  }

  /** Returns a single timer from the API as an observable.  */
  getTimer(id: number): Observable<UserData> {
    return this.http
      .get<UserData>("/api/productivity/" + id);
  }

  /** Creates a new timer and returns the created timer from the API as an observable. */
  createUser(request: UserData): Observable<UserData> {
    return this.http
      .post<UserData>("/api/productivity", request)
  }

  /** Edits a timer and returns the edited timer from the API as an observable. */
  editTimer(request: UserData): Observable<UserData> {
    return this.http
      .put<UserData>("/api/productivity", request)
  }

  /** Deletes a timer and returns the delete action as an observable. */
  deleteTimer(id: number) {
    return this.http.delete("/api/productivity/" + id);
  }

}
