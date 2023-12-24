import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PartOrderFormComponent } from './part-order-form.component';

describe('PartOrderFormComponent', () => {
  let component: PartOrderFormComponent;
  let fixture: ComponentFixture<PartOrderFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PartOrderFormComponent]
    });
    fixture = TestBed.createComponent(PartOrderFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
