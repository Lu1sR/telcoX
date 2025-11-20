/**
 * Shared Module
 * Contains shared components, directives, and pipes
 * Can be imported by feature modules
 */
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

// Components
import { LoadingSpinnerComponent } from './components/loading-spinner/loading-spinner.component';
import { ErrorMessageComponent } from './components/error-message/error-message.component';
import { EmptyStateComponent } from './components/empty-state/empty-state.component';
import { UsageCardComponent } from './components/usage-card/usage-card.component';

// Pipes
import { DataFormatPipe } from './pipes/data-format.pipe';
import { PercentageFormatPipe } from './pipes/percentage-format.pipe';
import { SafeNumberPipe } from './pipes/safe-number.pipe';

@NgModule({
  declarations: [
    // Components
    LoadingSpinnerComponent,
    ErrorMessageComponent,
    EmptyStateComponent,
    UsageCardComponent,
    // Pipes
    DataFormatPipe,
    PercentageFormatPipe,
    SafeNumberPipe
  ],
  imports: [
    CommonModule
  ],
  exports: [
    // Re-export CommonModule for convenience
    CommonModule,
    // Export components
    LoadingSpinnerComponent,
    ErrorMessageComponent,
    EmptyStateComponent,
    UsageCardComponent,
    // Export pipes
    DataFormatPipe,
    PercentageFormatPipe,
    SafeNumberPipe
  ]
})
export class SharedModule { }
