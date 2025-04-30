import { TestBed } from '@angular/core/testing';

import { StaffListService } from './staff-list.service';

describe('StaffListService', () => {
  let service: StaffListService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(StaffListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
