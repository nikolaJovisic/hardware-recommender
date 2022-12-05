import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { FormsModule } from '@angular/forms';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './app/navbar/navbar.component';
import { RecommandationComponent } from './app/page/recommandation/recommandation.component';
import { EvaluationComponent } from './app/page/evaluation/evaluation.component';
import { SimilaritiesComponent } from './app/page/similarities/similarities.component';
import { FailuresComponent } from './app/page/failures/failures.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    RecommandationComponent,
    EvaluationComponent,
    SimilaritiesComponent,
    FailuresComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
