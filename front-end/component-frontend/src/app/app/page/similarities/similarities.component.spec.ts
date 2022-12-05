import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SimilaritiesComponent } from './similarities.component';

describe('SimilaritiesComponent', () => {
  let component: SimilaritiesComponent;
  let fixture: ComponentFixture<SimilaritiesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SimilaritiesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SimilaritiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
