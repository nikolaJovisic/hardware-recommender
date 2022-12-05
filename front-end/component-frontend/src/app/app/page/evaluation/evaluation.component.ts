import { Component, OnInit } from '@angular/core';
import { ComponentService } from '../../services/component-service.service';

@Component({
  selector: 'app-evaluation',
  templateUrl: './evaluation.component.html',
  styleUrls: ['./evaluation.component.css']
})
export class EvaluationComponent implements OnInit {

  motherboards: string[] =[];
  cpus: string[] = [];
  gpus: string[] = [];
  ram: string[] = [];
  storage: string[] = [];
  results: any[] = [];
  displayResults: boolean = false;

  selectedComponents = {
    selectedMotherboard: 'Select motherboard',
    selectedCpu: 'Select cpu',
    selectedGpu: 'Select gpu',
    selectedRam: 'Select ram',
    selectedStorage: 'Select storage'
  };

  constructor(private _componentService: ComponentService) { }

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
    this._componentService.getConfigurationEvaluation(this.selectedComponents.selectedCpu, this.selectedComponents.selectedGpu, this.selectedComponents.selectedRam, this.selectedComponents.selectedStorage).subscribe({
      next: (value) => {this.results = value; this.displayResults = true;},
      error: (e) => alert("Please fill in the form")
    })
  }

}
