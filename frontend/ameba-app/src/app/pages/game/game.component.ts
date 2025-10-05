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
  template: `
    <div class="game-container">
      <mat-card class="game-card">
        <mat-card-header>
          <mat-card-title>
            <mat-icon>videogame_asset</mat-icon>
            Game Arena
            @if (isLoading()) {
              <mat-spinner diameter="20"></mat-spinner>
            }
          </mat-card-title>
          <mat-card-subtitle>
            @if (gameConfig()) {
              {{gameConfig()!.play_desk.rows}}×{{gameConfig()!.play_desk.columns}} simulation environment
            } @else {
              Ameba simulation environment
            }
          </mat-card-subtitle>
        </mat-card-header>
        
        <mat-card-content class="game-content">
          @if (isLoading()) {
            <div class="loading-state">
              <mat-spinner></mat-spinner>
              <p>Loading game configuration...</p>
            </div>
          } @else if (gameConfig()) {
            <!-- Game Statistics -->
            <div class="game-stats">
              <div class="stat-item">
                <mat-icon>energy_savings_leaf</mat-icon>
                <span>Energy per Food: {{gameConfig()!.play_desk.energy_per_food}}</span>
              </div>
              <div class="stat-item">
                <mat-icon>battery_full</mat-icon>
                <span>Total Energy: {{gameConfig()!.play_desk.total_energy}}</span>
              </div>
              <div class="stat-item">
                <mat-icon>visibility</mat-icon>
                <span>Ameba Vision: {{gameConfig()!.ameba.visible_rows}}×{{gameConfig()!.ameba.visible_columns}}</span>
              </div>
            </div>

            <!-- Game Grid -->
            <div class="game-grid-container">
              <table class="game-table">
                @for (row of getGameRows(); track $index) {
                  <tr class="game-row">
                    @for (cell of row; track cell.row + '-' + cell.col) {
                      <td class="game-cell" 
                          [ngClass]="getCellClass(cell)"
                          [title]="getCellTitle(cell)">
                        @switch (cell.type) {
                          @case ('ameba') {
                            <mat-icon class="cell-icon ameba-icon">pest_control</mat-icon>
                          }
                          @case ('food') {
                            <mat-icon class="cell-icon food-icon">local_dining</mat-icon>
                          }
                          @default {
                            <span class="empty-cell"></span>
                          }
                        }
                      </td>
                    }
                  </tr>
                }
              </table>
            </div>

            <!-- Game Info -->
            <div class="game-info">
              <p><strong>Amebas:</strong> {{getAmebaCount()}} | <strong>Food:</strong> {{getFoodCount()}} | <strong>Empty:</strong> {{getEmptyCount()}}</p>
            </div>
          } @else {
            <div class="error-state">
              <mat-icon>error</mat-icon>
              <p>Failed to load game configuration</p>
            </div>
          }
        </mat-card-content>
        
        <mat-card-actions class="game-actions">
          <button mat-raised-button color="primary" 
                  [disabled]="!gameConfig() || isGameRunning()"
                  (click)="startGame()">
            <mat-icon>play_arrow</mat-icon>
            Start Game
          </button>
          
          <button mat-raised-button color="warn"
                  [disabled]="!isGameRunning()"
                  (click)="stopGame()">
            <mat-icon>stop</mat-icon>
            Stop Game
          </button>
          
          <button mat-button (click)="resetGame()"
                  [disabled]="!gameConfig()">
            <mat-icon>refresh</mat-icon>
            Reset
          </button>
          
          <button mat-button (click)="loadConfiguration()">
            <mat-icon>settings</mat-icon>
            Reload Config
          </button>
          
          <button mat-stroked-button routerLink="/">
            <mat-icon>home</mat-icon>
            Back to Home
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
  styles: [`
    .game-container {
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 80vh;
      padding: 20px;
    }

    .game-card {
      max-width: 90vw;
      width: 100%;
    }

    .game-content {
      padding: 16px;
    }

    .loading-state, .error-state {
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 40px;
      text-align: center;
    }

    .loading-state mat-spinner {
      margin-bottom: 16px;
    }

    .error-state mat-icon {
      font-size: 48px;
      height: 48px;
      width: 48px;
      color: var(--mat-sys-error);
      margin-bottom: 16px;
    }

    mat-card-title {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Game Statistics */
    .game-stats {
      display: flex;
      justify-content: space-around;
      margin-bottom: 20px;
      padding: 12px;
      background: var(--mat-sys-surface-container-low);
      border-radius: 8px;
      flex-wrap: wrap;
      gap: 8px;
    }

    .stat-item {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 14px;
      color: var(--mat-sys-on-surface-variant);
    }

    .stat-item mat-icon {
      font-size: 16px;
      width: 16px;
      height: 16px;
    }

    /* Game Grid */
    .game-grid-container {
      display: flex;
      justify-content: center;
      margin: 20px 0;
      overflow: auto;
      max-height: 60vh;
    }

    .game-table {
      border-collapse: separate;
      border-spacing: 0;
      border: 3px solid var(--mat-sys-outline);
      border-radius: 8px;
      background-color: var(--mat-sys-outline-variant);
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      overflow: hidden;
      table-layout: fixed;
    }

    .game-row {
      
    }

    .game-cell {
      background-color: var(--mat-sys-surface);
      width: 30px;
      height: 30px;
      min-width: 30px;
      max-width: 30px;
      text-align: center;
      vertical-align: middle;
      position: relative;
      cursor: pointer;
      transition: all 0.2s ease;
      border-right: 1px solid var(--mat-sys-outline-variant);
      border-bottom: 1px solid var(--mat-sys-outline-variant);
      padding: 0;
      box-sizing: border-box;
    }

    .game-cell:first-child {
      border-left: 1px solid var(--mat-sys-outline-variant);
      width: 30px;
      min-width: 30px;
      max-width: 30px;
    }

    .game-row:first-child .game-cell {
      border-top: 1px solid var(--mat-sys-outline-variant);
    }

    .game-cell:hover {
      background-color: var(--mat-sys-surface-container);
      transform: scale(1.1);
      z-index: 1;
    }

    .empty-cell {
      background-color: var(--mat-sys-surface-container-lowest);
    }

    .food-cell {
      background: linear-gradient(135deg, #81C784, #A5D6A7, #C8E6C9);
      box-shadow: inset 0 2px 4px rgba(255, 255, 255, 0.5),
                  0 4px 8px rgba(129, 199, 132, 0.3);
      border: 2px solid #66BB6A;
    }

    .ameba-cell {
      background: radial-gradient(circle, #FFEB3B, #FFCC02, #FFC107);
      border: 2px solid #FF9800;
      box-shadow: 0 2px 6px rgba(255, 235, 59, 0.4),
                  inset 0 1px 3px rgba(255, 255, 255, 0.6);
      animation: glow 2s ease-in-out infinite alternate;
    }

    .cell-icon {
      font-size: 16px;
      width: 16px;
      height: 16px;
    }

    .food-icon {
      color: #1B5E20;
      text-shadow: 0 1px 2px rgba(255, 255, 255, 0.3);
      font-size: 16px !important;
      width: 16px !important;
      height: 16px !important;
      filter: drop-shadow(0 0 2px rgba(27, 94, 32, 0.8));
    }

    .ameba-icon {
      color: #8D4004;
      text-shadow: 0 1px 2px rgba(255, 255, 255, 0.5);
      font-size: 18px !important;
      width: 18px !important;
      height: 18px !important;
      filter: drop-shadow(0 0 3px rgba(141, 64, 4, 0.8));
    }

    .empty-cell {
      width: 100%;
      height: 100%;
    }

    /* Game Info */
    .game-info {
      text-align: center;
      margin: 16px 0;
      padding: 12px;
      background: var(--mat-sys-surface-container-low);
      border-radius: 8px;
      font-size: 14px;
    }

    /* Game Actions */
    .game-actions {
      display: flex;
      gap: 8px;
      justify-content: center;
      flex-wrap: wrap;
      padding: 16px;
    }

    .game-actions button {
      min-width: auto;
    }

    .game-actions button mat-icon {
      margin-right: 4px;
    }

    /* Animations */
    @keyframes glow {
      0% {
        box-shadow: 0 2px 6px rgba(255, 235, 59, 0.4),
                    inset 0 1px 3px rgba(255, 255, 255, 0.6);
      }
      100% {
        box-shadow: 0 4px 10px rgba(255, 235, 59, 0.6),
                    inset 0 2px 5px rgba(255, 255, 255, 0.8);
      }
    }

    /* Responsive Design */
    @media (max-width: 768px) {
      .game-container {
        padding: 16px;
      }

      .game-card {
        max-width: 95vw;
      }

      .game-stats {
        flex-direction: column;
        align-items: center;
      }

      .game-table {
        max-width: 90vw;
        max-height: 50vh;
      }

      .game-cell {
        width: 15px;
        height: 15px;
      }

      .cell-icon {
        font-size: 12px;
        width: 12px;
        height: 12px;
      }

      .game-actions {
        flex-direction: column;
      }

      .game-actions button {
        width: 100%;
      }
    }

    @media (max-width: 600px) {
      .game-container {
        padding: 8px;
      }

      .game-table {
        border-spacing: 0.5px;
      }

      .game-cell {
        width: 12px;
        height: 12px;
      }

      .cell-icon {
        font-size: 10px;
        width: 10px;
        height: 10px;
      }
    }

    /* Snackbar Styles */
    :host ::ng-deep {
      .success-snackbar {
        background-color: var(--mat-sys-primary);
        color: var(--mat-sys-on-primary);
      }

      .error-snackbar {
        background-color: var(--mat-sys-error);
        color: var(--mat-sys-on-error);
      }

      .info-snackbar {
        background-color: var(--mat-sys-tertiary);
        color: var(--mat-sys-on-tertiary);
      }
    }
  `]
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