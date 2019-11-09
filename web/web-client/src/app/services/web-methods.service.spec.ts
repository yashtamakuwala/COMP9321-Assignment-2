import { TestBed } from '@angular/core/testing';

import { WebMethodsService } from './web-methods.service';

describe('WebMethodsService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: WebMethodsService = TestBed.get(WebMethodsService);
    expect(service).toBeTruthy();
  });
});
