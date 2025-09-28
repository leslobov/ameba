import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

export interface TrainingRequest {
    steps: number;
    batch_size: number;
    mode: boolean;
}

export interface TrainingResponse {
    success: boolean;
    message: string;
    steps_completed?: number;
}

export interface TrainingStatus {
    model_exists: boolean;
    model_path: string;
    last_modified?: string;
    config_exists: boolean;
}

@Injectable({
    providedIn: 'root'
})
export class TrainingService {
    private http = inject(HttpClient);
    private readonly apiUrl = 'http://127.0.0.1:8000/api/training';

    /**
     * Start neural network training
     */
    startTraining(request: TrainingRequest): Observable<TrainingResponse> {
        return this.http.post<TrainingResponse>(`${this.apiUrl}/train`, request).pipe(
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Get training status and model information
     */
    getTrainingStatus(): Observable<TrainingStatus> {
        return this.http.get<TrainingStatus>(`${this.apiUrl}/status`).pipe(
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Error handler for HTTP requests
     */
    private handleError(error: HttpErrorResponse): Observable<never> {
        let errorMessage = 'An unknown error occurred';

        if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Error: ${error.error.message}`;
        } else {
            // Server-side error
            if (error.error?.detail) {
                errorMessage = error.error.detail;
            } else if (error.error?.message) {
                errorMessage = error.error.message;
            } else {
                errorMessage = `Error Code: ${error.status}\nMessage: ${error.message}`;
            }
        }

        console.error('Training Service Error:', errorMessage);
        return throwError(() => new Error(errorMessage));
    }
}