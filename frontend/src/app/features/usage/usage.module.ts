/**
 * Usage Module
 * Feature module for "My Usage" screen
 */
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { UsageRoutingModule } from './usage-routing.module';
import { UsageComponent } from './usage.component';
import { SharedModule } from '@shared/shared.module';

@NgModule({
  declarations: [
    UsageComponent
  ],
  imports: [
    CommonModule,
    FormsModule,  // For ngModel in customer ID selector
    UsageRoutingModule,
    SharedModule  // Import shared components and pipes
  ]
})
export class UsageModule { }
