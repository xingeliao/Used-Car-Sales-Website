import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewPartOrderComponent } from './view-part-order.component';

describe('PartOrderFormComponent', () => {
  let component: ViewPartOrderComponent;
  let fixture: ComponentFixture<ViewPartOrderComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ViewPartOrderComponent]
    });
    fixture = TestBed.createComponent(ViewPartOrderComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
