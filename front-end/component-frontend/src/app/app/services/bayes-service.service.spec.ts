import { TestBed } from '@angular/core/testing';

import { BayesService } from './bayes-service.service';

describe('BayesServiceService', () => {
  let service: BayesService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(BayesService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
