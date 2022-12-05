import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { EvaluationComponent } from './app/page/evaluation/evaluation.component';
import { FailuresComponent } from './app/page/failures/failures.component';
import { RecommandationComponent } from './app/page/recommandation/recommandation.component';
import { SimilaritiesComponent } from './app/page/similarities/similarities.component';

const routes: Routes = [
  {path: 'recommendation', component: RecommandationComponent},
  {path: 'evaluate', component: EvaluationComponent},
  {path: 'failures', component: FailuresComponent},
  {path: 'similiarities', component: SimilaritiesComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
