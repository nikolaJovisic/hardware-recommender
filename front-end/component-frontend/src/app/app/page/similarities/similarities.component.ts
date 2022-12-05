import { Component, OnInit } from '@angular/core';
import { ComponentService } from '../../services/component-service.service';
import { EvaluateService } from '../../services/evaluate.service';

@Component({
  selector: 'app-similarities',
  templateUrl: './similarities.component.html',
  styleUrls: ['./similarities.component.css']
})
export class SimilaritiesComponent implements OnInit {

  motherboards: string[] =[];
  cpus: string[] = [];
  gpus: string[] = [];
  ram: string[] = [];
  storage: string[] = [];
  results: any[] = [];
  displayResults: boolean = false;

  selectedComponents = {
    selectedCpu: 'Select cpu',
    selectedGpu: 'Select gpu',
    selectedRam: 'Select ram',
    selectedStorage: 'Select storage'
  };

  constructor(private _componentService: ComponentService,private _evaluateService: EvaluateService) { }

  ngOnInit(): void {
    this.getMotherboards();
    this.getCpus();
    this.getGpus();
    this.getRam();
    this.getStorage();
  }

  getMotherboards(){
    this._componentService.getComponent('Motherboard').subscribe({
      next: (value) => this.motherboards = value,
      error: (e) => console.log(e)
    });
  }

  getCpus(){
    this._componentService.getComponent('CPU').subscribe({
      next: (value) => this.cpus = value,
      error: (e) => console.log(e)
    });
  }

  getGpus(){
    this._componentService.getComponent('GraphicsCard').subscribe({
      next: (value) => this.gpus = value,
      error: (e) => console.log(e)
    });
  }

  getRam(){
    this._componentService.getComponent('RAM').subscribe({
      next: (value) => this.ram = value,
      error: (e) => console.log(e)
    });
  }

  getStorage(){
    this._componentService.getComponent('SSD').subscribe({
      next: (value) => this.storage = value,
      error: (e) => console.log(e)
    });
  }

  getResults(){
    this._evaluateService.getSimilarConfiguration(this.selectedComponents.selectedCpu,this.selectedComponents.selectedGpu,this.selectedComponents.selectedRam,this.selectedComponents.selectedStorage).subscribe({
      next: (value) => {this.results = value; this.displayResults = true;},
      error: (e) => alert("Please fill in the form!")
    })
  }

  

}
