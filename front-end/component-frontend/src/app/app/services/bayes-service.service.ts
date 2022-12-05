import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class BayesService {

  constructor(private http: HttpClient) { }

  private url: string = "/bayes";

  getAllSypmtoms(): Observable<string[]>{
    return this.http.get<string[]>(environment.host + this.url);
  }

  getAllCauses(syptom: string): Observable<string[]>{
    return this.http.get<string[]>(environment.host + this.url + '/causes' + `/${syptom}`);
  }

  getAdditionalSypmtoms(syptom: string): Observable<string[]>{
    return this.http.get<string[]>(environment.host + this.url + `/${syptom}`);
  }

  getResults(symptoms: string[], causes: string[]): Observable<any[]>{
    let queryDto: BayesQueryDTO;
    queryDto = {
      causes: causes,
      symptoms: symptoms
    }
    return this.http.post<any[]>(environment.host + this.url + '/complexQuery',queryDto);
  }

}

interface BayesQueryDTO{
  causes: string[];
  symptoms: string[];
}
