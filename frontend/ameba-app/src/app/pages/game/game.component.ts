import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, inject, OnDestroy, OnInit, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSliderModule } from '@angular/material/slider';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { RouterLink } from '@angular/router';
import { interval, Subscription } from 'rxjs';
import { GameState, MovementService, MoveRequest, SimulationRequest } from '../../services/movement.service';

// Game entities and types
interface GameConfig {
  play_desk: {
    rows: number;
    columns: number;
    total_energy: number;
    energy_per_food: number;
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
    input_size: number;
  };
}

interface Cell {
  row: number;
  col: number;
  type: 'empty' | 'food' | 'ameba';
  energy?: number;
}

@Component({
  selector: 'app-game',
  standalone: true,
  imports: [
    CommonModule,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatSnackBarModule,
    MatProgressSpinnerModule,
    MatSliderModule,
    MatChipsModule,
    RouterLink
  ],
  templateUrl: './game.component.html',
  styleUrl: './game.component.scss'
})
export class GameComponent implements OnInit, OnDestroy {
  private http = inject(HttpClient);
  private snackBar = inject(MatSnackBar);
  private movementService = inject(MovementService);

  // Reactive signals
  gameConfig = signal<GameConfig | null>(null);
  gameGrid = signal<Cell[]>([]);
  isLoading = signal<boolean>(true);
  isGameRunning = signal<boolean>(false);
  isMoving = signal<boolean>(false);
  simulationSpeed = signal<number>(1000); // milliseconds between moves
  autoMove = signal<boolean>(false);
  movementStats = signal<{ iterations: number, lastMoveTime: Date | null }>({
    iterations: 0,
    lastMoveTime: null
  });

  // Subscriptions
  private gameSubscription?: Subscription;
  private autoMoveSubscription?: Subscription;

  ngOnInit(): void {
    this.loadConfiguration();

    // Subscribe to movement service game state updates
    this.gameSubscription = this.movementService.gameState$.subscribe(gameState => {
      if (gameState) {
        this.updateGridFromGameState(gameState);
      }
    });
  }

  ngOnDestroy(): void {
    this.gameSubscription?.unsubscribe();
    this.autoMoveSubscription?.unsubscribe();
    this.stopAutoMove();
  }

  async loadConfiguration(): Promise<void> {
    this.isLoading.set(true);
    try {
      const response = await this.http.get<{ success: boolean, data: GameConfig }>('http://127.0.0.1:8000/api/config').toPromise();
      if (response?.success && response.data) {
        this.gameConfig.set(response.data);
        this.initializeGame();
        this.snackBar.open('Game configuration loaded successfully!', 'Close', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
      } else {
        throw new Error('Invalid response format');
      }
    } catch (error) {
      console.error('Failed to load configuration:', error);
      this.snackBar.open('Failed to load game configuration', 'Close', {
        duration: 5000,
        panelClass: ['error-snackbar']
      });
    } finally {
      this.isLoading.set(false);
    }
  }

  initializeGame(): void {
    const config = this.gameConfig();
    if (!config) return;

    const rows = config.play_desk.rows;
    const columns = config.play_desk.columns;
    const totalCells = rows * columns;
    const totalEnergy = config.play_desk.total_energy;
    const energyPerFood = config.play_desk.energy_per_food;

    // Calculate number of food items and amebas
    const foodCount = Math.floor(totalEnergy / energyPerFood);
    const amebaCount = Math.max(1, Math.floor(totalCells * 0.05)); // 5% of cells are amebas

    // Create empty grid
    const grid: Cell[] = [];
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < columns; col++) {
        grid.push({
          row,
          col,
          type: 'empty'
        });
      }
    }

    // Randomly place food
    const availablePositions = [...Array(totalCells).keys()];
    for (let i = 0; i < foodCount && availablePositions.length > 0; i++) {
      const randomIndex = Math.floor(Math.random() * availablePositions.length);
      const cellIndex = availablePositions.splice(randomIndex, 1)[0];
      grid[cellIndex].type = 'food';
      grid[cellIndex].energy = energyPerFood;
    }

    // Randomly place amebas
    for (let i = 0; i < amebaCount && availablePositions.length > 0; i++) {
      const randomIndex = Math.floor(Math.random() * availablePositions.length);
      const cellIndex = availablePositions.splice(randomIndex, 1)[0];
      grid[cellIndex].type = 'ameba';
      grid[cellIndex].energy = config.ameba.initial_energy;
    }

    this.gameGrid.set(grid);
  }

  getCellClass(cell: Cell): string {
    const baseClass = 'game-cell';
    switch (cell.type) {
      case 'ameba':
        return `${baseClass} ameba-cell`;
      case 'food':
        return `${baseClass} food-cell`;
      default:
        return `${baseClass} empty-cell`;
    }
  }

  getCellTitle(cell: Cell): string {
    switch (cell.type) {
      case 'ameba':
        return `Ameba at (${cell.row}, ${cell.col}) - Energy: ${cell.energy}`;
      case 'food':
        return `Food at (${cell.row}, ${cell.col}) - Energy: ${cell.energy}`;
      default:
        return `Empty cell at (${cell.row}, ${cell.col})`;
    }
  }

  getAmebaCount(): number {
    return this.gameGrid().filter(cell => cell.type === 'ameba').length;
  }

  getFoodCount(): number {
    return this.gameGrid().filter(cell => cell.type === 'food').length;
  }

  getEmptyCount(): number {
    return this.gameGrid().filter(cell => cell.type === 'empty').length;
  }

  getGameRows(): Cell[][] {
    const config = this.gameConfig();
    if (!config) return [];

    const rows: Cell[][] = [];
    const grid = this.gameGrid();

    for (let row = 0; row < config.play_desk.rows; row++) {
      const rowCells = grid.filter(cell => cell.row === row).sort((a, b) => a.col - b.col);
      rows.push(rowCells);
    }

    return rows;
  }

  startGame(): void {
    this.isGameRunning.set(true);
    this.snackBar.open('Game started! Amebas are now active.', 'Close', {
      duration: 3000,
      panelClass: ['success-snackbar']
    });
  }

  stopGame(): void {
    this.isGameRunning.set(false);
    this.stopAutoMove();
    this.snackBar.open('Game stopped.', 'Close', {
      duration: 2000,
      panelClass: ['info-snackbar']
    });
  }

  resetGame(): void {
    this.stopGame();
    this.initializeGame();
    this.movementStats.set({ iterations: 0, lastMoveTime: null });
    this.snackBar.open('Game reset to initial state.', 'Close', {
      duration: 2000,
      panelClass: ['info-snackbar']
    });
  }

  /**
   * Single step movement
   */
  async singleStep(): Promise<void> {
    if (this.isMoving() || !this.gameConfig()) return;

    this.isMoving.set(true);
    try {
      const gameState = this.movementService.convertToApiFormat(this.gameGrid(), this.gameConfig()!);
      const request: MoveRequest = {
        game_state: gameState,
        iterations: 1
      };

      const response = await this.movementService.moveAmebas(request).toPromise();
      if (response?.success) {
        const stats = this.movementStats();
        this.movementStats.set({
          iterations: stats.iterations + 1,
          lastMoveTime: new Date()
        });

        this.snackBar.open(`Movement completed! ${response.movements.length} amebas moved.`, 'Close', {
          duration: 2000,
          panelClass: ['success-snackbar']
        });
      }
    } catch (error) {
      console.error('Movement failed:', error);
      this.snackBar.open('Movement failed: ' + (error as Error).message, 'Close', {
        duration: 5000,
        panelClass: ['error-snackbar']
      });
    } finally {
      this.isMoving.set(false);
    }
  }

  /**
   * Start/stop automatic movement
   */
  toggleAutoMove(): void {
    if (this.autoMove()) {
      this.stopAutoMove();
    } else {
      this.startAutoMove();
    }
  }

  private startAutoMove(): void {
    if (this.autoMoveSubscription) return;

    this.autoMove.set(true);
    this.autoMoveSubscription = interval(this.simulationSpeed()).subscribe(async () => {
      if (this.isGameRunning() && !this.isMoving()) {
        await this.singleStep();
      }
    });

    this.snackBar.open('Auto movement started', 'Close', {
      duration: 2000,
      panelClass: ['success-snackbar']
    });
  }

  private stopAutoMove(): void {
    this.autoMove.set(false);
    this.autoMoveSubscription?.unsubscribe();
    this.autoMoveSubscription = undefined;
  }

  /**
   * Run a full simulation
   */
  async runFullSimulation(): Promise<void> {
    if (this.isMoving() || !this.gameConfig()) return;

    this.isMoving.set(true);
    try {
      const gameState = this.movementService.convertToApiFormat(this.gameGrid(), this.gameConfig()!);
      const request: SimulationRequest = {
        game_state: gameState,
        iterations: 50, // Run 50 iterations
        return_intermediate_states: false
      };

      const response = await this.movementService.runSimulation(request).toPromise();
      if (response?.success) {
        const stats = this.movementStats();
        this.movementStats.set({
          iterations: stats.iterations + response.total_iterations,
          lastMoveTime: new Date()
        });

        this.snackBar.open(
          `Simulation completed! ${response.total_iterations} iterations. Final: ${response.statistics.final_ameba_count} amebas, ${response.statistics.final_food_count} food`,
          'Close',
          {
            duration: 5000,
            panelClass: ['success-snackbar']
          }
        );
      }
    } catch (error) {
      console.error('Simulation failed:', error);
      this.snackBar.open('Simulation failed: ' + (error as Error).message, 'Close', {
        duration: 5000,
        panelClass: ['error-snackbar']
      });
    } finally {
      this.isMoving.set(false);
    }
  }

  /**
   * Update simulation speed
   */
  updateSimulationSpeed(speed: number): void {
    this.simulationSpeed.set(speed);
    if (this.autoMove()) {
      // Restart auto move with new speed
      this.stopAutoMove();
      this.startAutoMove();
    }
  }

  /**
   * Handle speed change from slider
   */
  onSpeedChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    const speed = parseInt(target.value, 10);
    this.updateSimulationSpeed(speed);
  }

  /**
   * Update grid from API game state
   */
  private updateGridFromGameState(gameState: GameState): void {
    const newGrid = this.movementService.convertFromApiFormat(gameState);
    this.gameGrid.set(newGrid);
  }
}