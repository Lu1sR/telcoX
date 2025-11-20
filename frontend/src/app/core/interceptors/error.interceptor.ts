/**
 * HTTP Error Interceptor
 * Handles HTTP errors globally and provides user-friendly error messages
 */
import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable()
export class ErrorInterceptor implements HttpInterceptor {

  constructor() {}

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    return next.handle(request).pipe(
      catchError((error: HttpErrorResponse) => {
        let errorMessage = 'An unknown error occurred';

        if (error.error instanceof ErrorEvent) {
          // Client-side error
          errorMessage = `Error: ${error.error.message}`;
          console.error('Client-side error:', error.error.message);
        } else {
          // Server-side error
          console.error(
            `Backend returned code ${error.status}, ` +
            `body was: ${JSON.stringify(error.error)}`
          );

          switch (error.status) {
            case 400:
              errorMessage = 'Bad Request - Please check your input';
              break;
            case 401:
              errorMessage = 'Unauthorized - Please login again';
              break;
            case 403:
              errorMessage = 'Forbidden - You don\'t have permission';
              break;
            case 404:
              errorMessage = 'Not Found - The requested resource does not exist';
              break;
            case 500:
              errorMessage = 'Internal Server Error - Please try again later';
              break;
            case 503:
              errorMessage = 'Service Unavailable - Please try again later';
              break;
            default:
              errorMessage = error.error?.message || error.message || errorMessage;
          }
        }

        // Log to console for debugging
        console.error('HTTP Error:', errorMessage);

        // Return error observable with user-friendly message
        return throwError(() => ({
          message: errorMessage,
          status: error.status,
          error: error.error
        }));
      })
    );
  }
}
