import { Injectable, Query } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ComponentService {

  private url: string = "/components"
  private url1: string = "/fuzzy"
  constructor(private http: HttpClient) { }

  getComponent(componentType: string): Observable<string[]>{
    return this.http.get<string[]>(environment.host + this.url + `/${componentType}`);
  }

  getUpgradeRecommendation(componentType: string, currentComponentName: string, motherboard: string): Observable<string[]>{
    let upgradeQueryDto: UpgradeQueryDTO;
    upgradeQueryDto = {
      componentType: componentType,
      currentComponentName: currentComponentName,
      motherboard: motherboard
    }
    return this.http.post<string[]>(environment.host + this.url + '/upgrade',upgradeQueryDto);
  }

  getConfigurationEvaluation(cpuName: string, gpuName: string, ramName: string, storageName: string): Observable<any[]>{
    let evaluateQueryDto: EvaluateQueryDTO;
    evaluateQueryDto = {
      cpuName: cpuName,
      gpuName: gpuName,
      ramName: ramName,
      storageName: storageName
    }
    return this.http.post<any[]>(environment.host + this.url1 + '/components', evaluateQueryDto);
  }

  getSimilarConfiguration(cpuName: string, gpuName: string, ramName: string, storageName: string){
    let similarQueryDTO: SimilarQueryDTO;
    similarQueryDTO = {
      cpuName: cpuName,
      gpuName: gpuName,
      ramName: ramName,
      storageName: storageName
    }
  }

  
}

interface UpgradeQueryDTO{
  componentType: string;
  currentComponentName: string;
  motherboard: string;
}

interface EvaluateQueryDTO{
  cpuName: string;
  gpuName: string;
  ramName: string;
  storageName: string;
}

interface SimilarQueryDTO{
  cpuName: string;
  gpuName: string;
  ramName: string;
  storageName: string;
}