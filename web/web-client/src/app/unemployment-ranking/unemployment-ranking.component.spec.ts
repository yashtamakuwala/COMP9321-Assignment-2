import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UnemploymentRankingComponent } from './unemployment-ranking.component';

describe('UnemploymentRankingComponent', () => {
  let component: UnemploymentRankingComponent;
  let fixture: ComponentFixture<UnemploymentRankingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UnemploymentRankingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UnemploymentRankingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
