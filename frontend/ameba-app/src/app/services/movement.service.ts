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

export interface MoveResponse {
    success: boolean;
    message: string;
    movements: MovementResult[];
    updated_game_state?: GameState;
    iterations_completed: number;
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
        const totalCells = gameState.board_size.rows * gameState.board_size.columns;

        // Initialize empty grid
        for (let row = 0; row < gameState.board_size.rows; row++) {
            for (let col = 0; col < gameState.board_size.columns; col++) {
                grid.push({
                    row,
                    col,
                    type: 'empty'
                });
            }
        }

        // Place amebas
        gameState.amebas.forEach(ameba => {
            const index = ameba.position.row * gameState.board_size.columns + ameba.position.column;
            if (index >= 0 && index < totalCells) {
                grid[index] = {
                    row: ameba.position.row,
                    col: ameba.position.column,
                    type: 'ameba',
                    energy: ameba.energy
                };
            }
        });

        // Place foods
        gameState.foods.forEach(food => {
            const index = food.position.row * gameState.board_size.columns + food.position.column;
            if (index >= 0 && index < totalCells) {
                grid[index] = {
                    row: food.position.row,
                    col: food.position.column,
                    type: 'food',
                    energy: food.energy
                };
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