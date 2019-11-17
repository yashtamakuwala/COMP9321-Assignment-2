import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { RatingRankingComponent } from './rating-ranking.component';

describe('RatingRankingComponent', () => {
  let component: RatingRankingComponent;
  let fixture: ComponentFixture<RatingRankingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ RatingRankingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(RatingRankingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
