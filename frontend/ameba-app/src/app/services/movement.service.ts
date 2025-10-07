import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { BehaviorSubject, Observable, throwError } from 'rxjs';
import { catchError, tap } from 'rxjs/operators';

export interface Position {
    row: number;
    column: number;
}

export interface CellEntity {
    type: 'empty' | 'food' | 'ameba';
    energy?: number;
    position: Position;
}

export interface GameState {
    amebas: CellEntity[];
    foods: CellEntity[];
    board_size: {
        rows: number;
        columns: number;
    };
}

export interface MovementResult {
    ameba_position: Position;
    old_position: Position;
    new_position: Position;
    energy_change: number;
    food_consumed?: Position;
}

export interface MoveRequest {
    game_state: GameState;
    ameba_id?: number;
    iterations: number;
}

export interface FoodGenerationInfo {
    total_foods_consumed: number;
    total_foods_generated: number;
    net_food_change: number;
}

export interface MoveResponse {
    success: boolean;
    message: string;
    movements: MovementResult[];
    updated_game_state?: GameState;
    iterations_completed: number;
    food_generation?: FoodGenerationInfo;
}

export interface SimulationRequest {
    game_state: GameState;
    iterations: number;
    return_intermediate_states?: boolean;
}

export interface SimulationResponse {
    success: boolean;
    message: string;
    total_iterations: number;
    final_game_state: GameState;
    steps?: GameState[];
    statistics: {
        final_ameba_count: number;
        final_food_count: number;
        total_energy: number;
    };
}

export interface MovementStatus {
    game_loaded: boolean;
    ameba_count: number;
    food_count: number;
    board_size: {
        rows: number;
        columns: number;
    };
    message: string;
}

export interface GameStateResponse {
    success: boolean;
    message: string;
    game_state: GameState;
    ameba_count: number;
    food_count: number;
    board_size: {
        rows: number;
        columns: number;
    };
}

@Injectable({
    providedIn: 'root'
})
export class MovementService {
    private readonly http = inject(HttpClient);
    private readonly apiBaseUrl = 'http://127.0.0.1:8000/api/movement';

    // Observable for game state changes
    private readonly gameStateSubject = new BehaviorSubject<GameState | null>(null);
    public readonly gameState$ = this.gameStateSubject.asObservable();

    // Observable for movement status
    private readonly movementStatusSubject = new BehaviorSubject<MovementStatus | null>(null);
    public readonly movementStatus$ = this.movementStatusSubject.asObservable();

    constructor() {
        this.checkMovementStatus();
    }

    /**
     * Check movement system status
     */
    checkMovementStatus(): Observable<MovementStatus> {
        return this.http.get<MovementStatus>(`${this.apiBaseUrl}/status`).pipe(
            tap(status => this.movementStatusSubject.next(status)),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Move amebas one or more iterations
     */
    moveAmebas(request: MoveRequest): Observable<MoveResponse> {
        return this.http.post<MoveResponse>(`${this.apiBaseUrl}/move`, request).pipe(
            tap(response => {
                if (response.success && response.updated_game_state) {
                    this.gameStateSubject.next(response.updated_game_state);
                }
            }),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Run a full simulation
     */
    runSimulation(request: SimulationRequest): Observable<SimulationResponse> {
        return this.http.post<SimulationResponse>(`${this.apiBaseUrl}/simulate`, request).pipe(
            tap(response => {
                if (response.success && response.final_game_state) {
                    this.gameStateSubject.next(response.final_game_state);
                }
            }),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Get the current backend game state from the Game class PlayDesk
     */
    getBackendGameState(): Observable<GameStateResponse> {
        return this.http.get<GameStateResponse>(`${this.apiBaseUrl}/state`).pipe(
            tap(response => {
                if (response.success && response.game_state) {
                    this.gameStateSubject.next(response.game_state);
                }
            }),
            catchError(this.handleError.bind(this))
        );
    }

    /**
     * Convert frontend cell format to API format
     */
    convertToApiFormat(grid: any[], config: any): GameState {
        const amebas: CellEntity[] = [];
        const foods: CellEntity[] = [];

        grid.forEach(cell => {
            if (cell.type === 'ameba') {
                amebas.push({
                    type: 'ameba',
                    energy: cell.energy || 100,
                    position: { row: cell.row, column: cell.col }
                });
            } else if (cell.type === 'food') {
                foods.push({
                    type: 'food',
                    energy: cell.energy || 50,
                    position: { row: cell.row, column: cell.col }
                });
            }
        });

        return {
            amebas,
            foods,
            board_size: {
                rows: config.play_desk.rows,
                columns: config.play_desk.columns
            }
        };
    }

    /**
     * Convert API format back to frontend cell format
     */
    convertFromApiFormat(gameState: GameState): any[] {
        const grid: any[] = [];
        const rows = gameState.board_size.rows;
        const columns = gameState.board_size.columns;

        // Initialize empty grid with proper row/column structure
        for (let row = 0; row < rows; row++) {
            for (let col = 0; col < columns; col++) {
                grid.push({
                    row: row,
                    col: col,
                    type: 'empty'
                });
            }
        }

        // Place amebas - with bounds checking
        gameState.amebas.forEach(ameba => {
            const row = ameba.position.row;
            const col = ameba.position.column;

            // Check bounds to prevent invalid positions
            if (row >= 0 && row < rows && col >= 0 && col < columns) {
                const index = row * columns + col;
                if (index >= 0 && index < grid.length) {
                    grid[index] = {
                        row: row,
                        col: col,
                        type: 'ameba',
                        energy: ameba.energy || 100
                    };
                }
            } else {
                console.warn(`Invalid ameba position: (${row}, ${col}) - bounds: ${rows}x${columns}`);
            }
        });

        // Place foods - with bounds checking
        gameState.foods.forEach(food => {
            const row = food.position.row;
            const col = food.position.column;

            // Check bounds to prevent invalid positions
            if (row >= 0 && row < rows && col >= 0 && col < columns) {
                const index = row * columns + col;
                if (index >= 0 && index < grid.length) {
                    grid[index] = {
                        row: row,
                        col: col,
                        type: 'food',
                        energy: food.energy || 50
                    };
                }
            } else {
                console.warn(`Invalid food position: (${row}, ${col}) - bounds: ${rows}x${columns}`);
            }
        });

        return grid;
    }

    /**
     * Get current game state
     */
    getCurrentGameState(): GameState | null {
        return this.gameStateSubject.value;
    }

    /**
     * Set current game state
     */
    setCurrentGameState(gameState: GameState): void {
        this.gameStateSubject.next(gameState);
    }

    private handleError(error: HttpErrorResponse): Observable<never> {
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

        console.error('Movement API Error:', errorMessage);
        return throwError(() => new Error(errorMessage));
    }
}