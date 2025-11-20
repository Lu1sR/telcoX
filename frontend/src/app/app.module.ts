/**
 * App Module - Root module of the application
 */
import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

// Core Module - import only once
import { CoreModule } from './core/core.module';

// Shared Module
import { SharedModule } from './shared/shared.module';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    CoreModule,      // Import CoreModule (contains HttpClient, interceptors, services)
    SharedModule     // Import SharedModule (shared components, directives, pipes)
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
