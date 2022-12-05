import { Component, OnInit } from '@angular/core';
import { BayesService } from '../../services/bayes-service.service';

@Component({
  selector: 'app-failures',
  templateUrl: './failures.component.html',
  styleUrls: ['./failures.component.css']
})
export class FailuresComponent implements OnInit {

  symptoms: string[] = [];
  results: any[] = []
  additionalSypmtoms: string[] = [];
  causes: string[] = [];
  displayResults: boolean = false;
  

  selectedSymptom: string = "Select symptom"
  selectedSymptoms: string[] = [];
  selectedCauses: string[] = [];

  constructor(private _bayesService: BayesService) { }

  ngOnInit(): void {
    this.getAllSymptoms();
  }

  onChange(): void{
    this._bayesService.getAdditionalSypmtoms(this.selectedSymptom).subscribe({
      next: (value) => this.additionalSypmtoms = value.filter(x => x!=this.selectedSymptom),
      error: (e) => console.log(e)
    })

    this._bayesService.getAllCauses(this.selectedSymptom).subscribe({
      next: (value) => this.causes = value,
      error: (e) => console.log(e)
    })

  }


  getResults(){
    this.displayResults = true;
    if(!this.selectedSymptoms.includes(this.selectedSymptom))
      this.selectedSymptoms = this.selectedSymptoms.concat(this.selectedSymptom);
    this._bayesService.getResults(this.selectedSymptoms,this.selectedCauses).subscribe({
      next: (value) => this.results = value,
      error: (e) => console.log(e)
    })
  }

  getAllSymptoms(){
    this._bayesService.getAllSypmtoms().subscribe({
      next: (value) => this.symptoms = value,
      error: (e) => console.log(e)
    })
  }

  addSymptom(event: any, symptom: string){
    if(event.target.checked)
      this.selectedSymptoms = this.selectedSymptoms.concat(symptom);
    else
      this.selectedSymptoms = this.selectedSymptoms.filter(x => x!=symptom);
  }

  addCause(event: any, cause: string){
    if(event.target.checked)
      this.selectedCauses = this.selectedCauses.concat(cause);
    else
      this.selectedCauses = this.selectedCauses.filter(x => x!=cause);
  }

}
