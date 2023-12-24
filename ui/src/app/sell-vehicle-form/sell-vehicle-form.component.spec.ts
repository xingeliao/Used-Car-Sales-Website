import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SellVehicleFormComponent } from './sell-vehicle-form.component';

describe('SellVehicleFormComponent', () => {
  let component: SellVehicleFormComponent;
  let fixture: ComponentFixture<SellVehicleFormComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [SellVehicleFormComponent]
    });
    fixture = TestBed.createComponent(SellVehicleFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
