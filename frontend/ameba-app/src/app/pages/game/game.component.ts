import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { RouterLink } from '@angular/router';

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
    RouterLink
  ],
  templateUrl: './game.component.html',
  styleUrl: './game.component.scss'
})
export class GameComponent implements OnInit {
  private http = inject(HttpClient);
  private snackBar = inject(MatSnackBar);

  // Reactive signals
  gameConfig = signal<GameConfig | null>(null);
  gameGrid = signal<Cell[]>([]);
  isLoading = signal<boolean>(true);
  isGameRunning = signal<boolean>(false);

  ngOnInit(): void {
    this.loadConfiguration();
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
    // TODO: Implement actual game logic / simulation loop
  }

  stopGame(): void {
    this.isGameRunning.set(false);
    this.snackBar.open('Game stopped.', 'Close', {
      duration: 2000,
      panelClass: ['info-snackbar']
    });
  }

  resetGame(): void {
    this.stopGame();
    this.initializeGame();
    this.snackBar.open('Game reset to initial state.', 'Close', {
      duration: 2000,
      panelClass: ['info-snackbar']
    });
  }
}