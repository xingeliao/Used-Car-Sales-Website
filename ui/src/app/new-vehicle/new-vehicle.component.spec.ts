import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NewVehicleComponent } from './new-vehicle.component';

describe('NewVehicleComponent', () => {
  let component: NewVehicleComponent;
  let fixture: ComponentFixture<NewVehicleComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [NewVehicleComponent]
    });
    fixture = TestBed.createComponent(NewVehicleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
