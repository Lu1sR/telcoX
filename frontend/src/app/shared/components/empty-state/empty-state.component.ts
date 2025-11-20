/**
 * Empty State Component
 * Displays a message when no data is available
 */
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-empty-state',
  templateUrl: './empty-state.component.html',
  styleUrls: ['./empty-state.component.scss']
})
export class EmptyStateComponent {
  @Input() title = 'No Data Available';
  @Input() description?: string;
  @Input() icon = '📭';
}
