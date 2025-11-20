/**
 * Loading Interceptor
 * Manages global loading state for HTTP requests
 */
import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpResponse
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap, finalize } from 'rxjs/operators';
import { LoadingService } from '../services/loading.service';

@Injectable()
export class LoadingInterceptor implements HttpInterceptor {

  constructor(private loadingService: LoadingService) {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    // Show loading indicator
    this.loadingService.show();

    return next.handle(request).pipe(
      tap((event: HttpEvent<any>) => {
        // Optional: Do something with successful response
        if (event instanceof HttpResponse) {
          // console.log('HTTP Response received');
        }
      }),
      finalize(() => {
        // Hide loading indicator when request completes (success or error)
        this.loadingService.hide();
      })
    );
  }
}
