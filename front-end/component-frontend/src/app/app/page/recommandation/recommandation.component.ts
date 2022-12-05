import { Component, OnInit } from '@angular/core';
import { ComponentService } from '../../services/component-service.service';

@Component({
  selector: 'app-recommandation',
  templateUrl: './recommandation.component.html',
  styleUrls: ['./recommandation.component.css']
})
export class RecommandationComponent implements OnInit {

  motherboards: string[] =[];
  cpus: string[] = [];
  gpus: string[] = [];
  ram: string[] = [];
  storage: string[] = [];
  components: string[] = ['CPU','GraphicsCard','RAM','SSD'];
  results: string[] = [];
  displayResults: boolean = false;

  selectedComponents = {
    selectedMotherboard: 'Select motherboard',
    selectedCpu: 'Select cpu',
    selectedGpu: 'Select gpu',
    selectedRam: 'Select ram',
    selectedStorage: 'Select storage',
    selectedComponent: 'Select component'
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
    let relevantComponent = "";
    switch(this.selectedComponents.selectedComponent){
      case "CPU": relevantComponent = this.selectedComponents.selectedCpu; break;
      case "GraphicsCard": relevantComponent = this.selectedComponents.selectedGpu; break;
      case "RAM": relevantComponent = this.selectedComponents.selectedRam; break;
      case "SSD": relevantComponent = this.selectedComponents.selectedStorage; break;
      default: alert("Please choose component!");
    }
    this._componentService.getUpgradeRecommendation(this.selectedComponents.selectedComponent,relevantComponent,this.selectedComponents.selectedMotherboard).subscribe({
      next: (value) => {this.results = value; this.displayResults = true;},
      error: (e) => alert("Please fill in the form"!)
    });
  }

}
