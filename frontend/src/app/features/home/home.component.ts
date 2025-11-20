/**
 * Home Component - Placeholder for Phase 4
 */
import { Component, OnInit } from '@angular/core';
import { UsageService } from '@core/services/usage.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  constructor(private usageService: UsageService) { }

  ngOnInit(): void {
    // Test API call - will fetch customer 1's usage data
    // This demonstrates that services are working
    console.log('HomeComponent initialized. Services are ready.');
    
    // Uncomment to test API call:
    // this.usageService.getCustomerUsageOverview(1).subscribe({
    //   next: (data) => console.log('API Response:', data),
    //   error: (err) => console.error('API Error:', err)
    // });
  }

}
