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
    // Temporarily disabled to prevent automatic updates that might cause issues
    // this.gameSubscription = this.movementService.gameState$.subscribe(gameState => {
    //   if (gameState) {
    //     this.updateGridFromGameState(gameState);
    //   }
    // });
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
    const expectedRows = config.play_desk.rows;
    const expectedCols = config.play_desk.columns;

    // Create rows matrix ensuring all rows exist
    for (let row = 0; row < expectedRows; row++) {
      const rowCells = grid.filter(cell => cell.row === row).sort((a, b) => a.col - b.col);

      // Ensure each row has the expected number of columns
      if (rowCells.length !== expectedCols) {
        console.warn(`Row ${row} has ${rowCells.length} cells, expected ${expectedCols}`);

        // Fill missing cells if needed
        const fullRow: Cell[] = [];
        for (let col = 0; col < expectedCols; col++) {
          const existingCell = rowCells.find(cell => cell.col === col);
          if (existingCell) {
            fullRow.push(existingCell);
          } else {
            // Create missing empty cell
            fullRow.push({
              row: row,
              col: col,
              type: 'empty'
            });
          }
        }
        rows.push(fullRow);
      } else {
        rows.push(rowCells);
      }
    }

    // Debug check
    if (rows.length !== expectedRows) {
      console.error(`getGameRows returned ${rows.length} rows, expected ${expectedRows}`);
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
      const currentGrid = this.gameGrid();
      const gameState = this.movementService.convertToApiFormat(currentGrid, this.gameConfig()!);

      console.log('Before movement:', {
        gridCells: currentGrid.length,
        amebas: gameState.amebas.length,
        foods: gameState.foods.length,
        boardSize: gameState.board_size
      });

      const request: MoveRequest = {
        game_state: gameState,
        iterations: 1
      };

      const response = await this.movementService.moveAmebas(request).toPromise();
      if (response?.success) {
        console.log('Movement response:', {
          movements: response.movements.length,
          updatedState: response.updated_game_state ? {
            amebas: response.updated_game_state.amebas.length,
            foods: response.updated_game_state.foods.length,
            boardSize: response.updated_game_state.board_size
          } : null
        });

        // Manually update the grid to ensure consistency
        if (response.updated_game_state) {
          this.updateGridFromGameState(response.updated_game_state);
        }

        const stats = this.movementStats();
        this.movementStats.set({
          iterations: stats.iterations + 1,
          lastMoveTime: new Date()
        });

        this.snackBar.open(`Movement completed! ${response.movements.length} amebas moved.`, 'Close', {
          duration: 2000,
          panelClass: ['success-snackbar']
        });
      } else {
        console.error('Movement failed:', response?.message);
        this.snackBar.open('Movement failed: ' + (response?.message || 'Unknown error'), 'Close', {
          duration: 5000,
          panelClass: ['error-snackbar']
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
    const config = this.gameConfig();
    if (!config) {
      console.error('No game config available for grid update');
      return;
    }

    console.log('Updating grid from API state:', {
      apiState: gameState.board_size,
      configSize: { rows: config.play_desk.rows, columns: config.play_desk.columns },
      amebas: gameState.amebas.length,
      foods: gameState.foods.length
    });

    // Use config dimensions instead of API dimensions to maintain consistency
    const newGrid = this.convertApiToGrid(gameState, config);

    // Verify the grid has the correct number of cells
    const expectedCells = config.play_desk.rows * config.play_desk.columns;
    if (newGrid.length !== expectedCells) {
      console.error('Grid size mismatch:', {
        expected: expectedCells,
        actual: newGrid.length,
        dimensions: `${config.play_desk.rows}x${config.play_desk.columns}`
      });
      return;
    }

    this.gameGrid.set(newGrid);

    // Debug info
    console.log('Grid updated successfully:', {
      amebas: this.getAmebaCount(),
      food: this.getFoodCount(),
      empty: this.getEmptyCount(),
      total: newGrid.length,
      rowsInDisplay: this.getGameRows().length
    });
  }

  /**
   * Convert API game state to frontend grid using config dimensions
   */
  private convertApiToGrid(gameState: GameState, config: GameConfig): Cell[] {
    const grid: Cell[] = [];
    const rows = config.play_desk.rows;
    const columns = config.play_desk.columns;

    // Initialize empty grid based on config dimensions (not API dimensions)
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < columns; col++) {
        grid.push({
          row: row,
          col: col,
          type: 'empty'
        });
      }
    }

    // Place amebas - with bounds checking against config dimensions
    gameState.amebas.forEach(ameba => {
      const row = ameba.position.row;
      const col = ameba.position.column;

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
        console.warn(`Invalid ameba position: (${row}, ${col}) - config bounds: ${rows}x${columns}`);
      }
    });

    // Place foods - with bounds checking against config dimensions
    gameState.foods.forEach(food => {
      const row = food.position.row;
      const col = food.position.column;

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
        console.warn(`Invalid food position: (${row}, ${col}) - config bounds: ${rows}x${columns}`);
      }
    });

    return grid;
  }
}