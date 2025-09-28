import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

export interface BackendGameConfig {
    play_desk: {
        total_energy: number;
        energy_per_food: number;
        rows: number;
        columns: number;
    };
    ameba: {
        threhold_of_lostness_weight_coefficient: number;
        visible_rows: number;
        visible_columns: number;
        initial_energy: number;
        lost_energy_per_move: number;
    };
    neural_network: {
        initial_hidden_layers: number;
        initial_neurons_on_layer: number;
    };
}

export interface ApiResponse<T> {
    success: boolean;
    data: T;
    message: string;
}

@Injectable({
    providedIn: 'root'
})
export class BackendApiService {
    private readonly http = inject(HttpClient);
    private readonly apiBaseUrl = 'http://127.0.0.1:8000/api';

    // Observable for connection status
    private readonly connectionStatusSubject = new BehaviorSubject<boolean>(false);
    public readonly connectionStatus$ = this.connectionStatusSubject.asObservable();

    constructor() {
        this.checkConnection();
    }

    /**
     * Check if the API server is accessible
     */
    checkConnection(): Observable<boolean> {
        return this.http.get(`http://127.0.0.1:8000/health`).pipe(
            map(() => {
                this.connectionStatusSubject.next(true);
                return true;
            }),
            catchError(() => {
                this.connectionStatusSubject.next(false);
                return throwError(() => new Error('API server not accessible'));
            })
        );
    }

    /**
     * Get the complete game configuration from backend
     */
    getGameConfig(): Observable<BackendGameConfig> {
        return this.http.get<ApiResponse<BackendGameConfig>>(`${this.apiBaseUrl}/config`).pipe(
            map(response => response.data),
            tap(() => this.connectionStatusSubject.next(true)),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Update the complete game configuration
     */
    updateGameConfig(config: BackendGameConfig): Observable<BackendGameConfig> {
        return this.http.put<ApiResponse<BackendGameConfig>>(`${this.apiBaseUrl}/config`, config).pipe(
            map(response => response.data),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Get specific configuration section
     */
    getConfigSection(section: 'play_desk' | 'ameba' | 'neural_network'): Observable<any> {
        return this.http.get<ApiResponse<any>>(`${this.apiBaseUrl}/config/${section}`).pipe(
            map(response => response.data),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Update specific configuration section
     */
    updateConfigSection(section: 'play_desk' | 'ameba' | 'neural_network', sectionData: any): Observable<any> {
        return this.http.put<ApiResponse<any>>(`${this.apiBaseUrl}/config/${section}`, sectionData).pipe(
            map(response => response.data),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Reset configuration to defaults
     */
    resetConfigToDefaults(): Observable<BackendGameConfig> {
        return this.http.post<ApiResponse<BackendGameConfig>>(`${this.apiBaseUrl}/config/reset`, {}).pipe(
            map(response => response.data),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Convert backend config to frontend format
     */
    mapBackendToFrontend(backendConfig: BackendGameConfig): any {
        return {
            worldWidth: backendConfig.play_desk.columns * 25, // Convert grid to pixels
            worldHeight: backendConfig.play_desk.rows * 25,
            initialAmebaCount: 20, // Default, not in backend config
            initialFoodCount: Math.floor(backendConfig.play_desk.total_energy / backendConfig.play_desk.energy_per_food),
            maxSimulationSpeed: 3, // Default
            energyDecayRate: backendConfig.ameba.lost_energy_per_move,
            reproductionThreshold: backendConfig.ameba.initial_energy,
            mutationRate: 0.1, // Default
            enableNeuralNetwork: true,
            networkComplexity: this.mapNetworkComplexity(backendConfig.neural_network.initial_hidden_layers),
            autoSave: true
        };
    }

    /**
     * Convert frontend config to backend format
     */
    mapFrontendToBackend(frontendConfig: any): BackendGameConfig {
        return {
            play_desk: {
                total_energy: frontendConfig.initialFoodCount * 50, // 50 energy per food
                energy_per_food: 50,
                rows: Math.floor(frontendConfig.worldHeight / 25),
                columns: Math.floor(frontendConfig.worldWidth / 25)
            },
            ameba: {
                threhold_of_lostness_weight_coefficient: 0.2,
                visible_rows: 5,
                visible_columns: 5,
                initial_energy: frontendConfig.reproductionThreshold,
                lost_energy_per_move: frontendConfig.energyDecayRate
            },
            neural_network: {
                initial_hidden_layers: this.mapComplexityToLayers(frontendConfig.networkComplexity),
                initial_neurons_on_layer: 32
            }
        };
    }

    private mapNetworkComplexity(layers: number): string {
        if (layers <= 1) return 'simple';
        if (layers <= 2) return 'medium';
        return 'complex';
    }

    private mapComplexityToLayers(complexity: string): number {
        switch (complexity) {
            case 'simple': return 1;
            case 'medium': return 2;
            case 'complex': return 3;
            default: return 2;
        }
    }

    private handleError(error: HttpErrorResponse): Observable<never> {
        this.connectionStatusSubject.next(false);

        let errorMessage = 'An unknown error occurred';

        if (error.error instanceof ErrorEvent) {
            // Client-side error
            errorMessage = `Client Error: ${error.error.message}`;
        } else {
            // Server-side error
            errorMessage = `Server Error: ${error.status} - ${error.message}`;
            if (error.error?.detail) {
                errorMessage += ` - ${error.error.detail}`;
            }
        }

        console.error('API Error:', errorMessage);
        return throwError(() => new Error(errorMessage));
    }
}