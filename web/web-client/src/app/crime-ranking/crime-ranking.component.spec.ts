import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CrimeRankingComponent } from './crime-ranking.component';

describe('CrimeRankingComponent', () => {
  let component: CrimeRankingComponent;
  let fixture: ComponentFixture<CrimeRankingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CrimeRankingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CrimeRankingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
