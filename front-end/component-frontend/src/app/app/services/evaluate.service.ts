import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class EvaluateService {

  constructor(private http: HttpClient) { }

  private url: string = '/evaluate';

  getSimilarConfiguration(cpuName: string, gpuName: string, ramName: string, storageName: string): Observable<any[]>{
    let similarQueryDTO: SimilarQueryDTO;
    similarQueryDTO = {
      cpuName: cpuName,
      gpuName: gpuName,
      ramName: ramName,
      storageName: storageName
    }

    return this.http.post<any[]>(environment.host + this.url,similarQueryDTO);
  }

}

interface SimilarQueryDTO{
  cpuName: string;
  gpuName: string;
  ramName: string;
  storageName: string;
}
