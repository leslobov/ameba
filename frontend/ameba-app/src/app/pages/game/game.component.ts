import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { RouterLink } from '@angular/router';

@Component({
    selector: 'app-game',
    imports: [MatButtonModule, MatCardModule, MatIconModule, RouterLink],
    template: `
    <div class="flex-center mat-padding-lg">
      <mat-card class="mat-card-center">
        <mat-card-header>
          <mat-card-title>
            <mat-icon>videogame_asset</mat-icon>
            Game Arena
          </mat-card-title>
          <mat-card-subtitle>Ameba simulation environment</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content class="mat-padding-v-md">
          <div class="game-area">
            <p>Game simulation will be displayed here.</p>
            <div class="simulation-placeholder">
              🦠 🦠 🦠<br>
              🦠 🟢 🦠<br>
              🦠 🦠 🦠
            </div>
          </div>
        </mat-card-content>
        <mat-card-actions class="flex-center-horizontal mat-padding-sm" style="gap: 16px;">
          <button mat-fab color="primary" aria-label="Start">
            <mat-icon>play_arrow</mat-icon>
          </button>
          <button mat-fab color="warn" aria-label="Stop">
            <mat-icon>stop</mat-icon>
          </button>
          <button mat-stroked-button routerLink="/">
            Back to Home
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
    styles: [`
    mat-card {
      max-width: 500px;
    }
    .game-area {
      text-align: center;
    }
    .simulation-placeholder {
      font-size: 24px;
      line-height: 1.2;
      padding: 20px;
      background: #f5f5f5;
      border-radius: 8px;
      margin: 16px 0;
    }
    mat-card-title {
      display: flex;
      align-items: center;
      gap: 8px;
    }
  `]
})
export class GameComponent { }