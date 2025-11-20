/**
 * App Routing Module
 * Defines application routes
 */
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

const routes: Routes = [
  // Default route - redirect to usage
  {
    path: '',
    redirectTo: '/usage',
    pathMatch: 'full'
  },
  // Placeholder home route
  {
    path: 'home',
    loadChildren: () => import('./features/home/home.module').then(m => m.HomeModule)
  },
  // My Usage route (Phase 5)
  {
    path: 'usage',
    loadChildren: () => import('./features/usage/usage.module').then(m => m.UsageModule)
  },
  // Wildcard route
  {
    path: '**',
    redirectTo: '/usage'
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
