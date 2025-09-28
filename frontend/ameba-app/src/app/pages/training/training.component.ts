import { Component, OnInit, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Router } from '@angular/router';

@Component({
    selector: 'app-training',
    standalone: true,
    imports: [
        MatButtonModule,
        MatCardModule,
        MatIconModule,
        MatSnackBarModule
    ],
    template: `
    <div class="training-container">
      <mat-card class="training-card">
        <mat-card-header>
          <mat-icon mat-card-avatar color="accent">psychology</mat-icon>
          <mat-card-title>Neural Network Training</mat-card-title>
          <mat-card-subtitle>Train your ameba with the configured game settings</mat-card-subtitle>
        </mat-card-header>

        <mat-card-content>
          @if (gameConfig) {
            <div class="config-info">
              <h3>Training Configuration Received</h3>
              <p>A new game configuration has been provided for training.</p>
              <ul>
                <li>Game Board: {{gameConfig.play_desk.rows}}×{{gameConfig.play_desk.columns}}</li>
                <li>Population Size: {{gameConfig.neural_network.initial_neurons_on_layer}}</li>
                <li>Energy per Food: {{gameConfig.play_desk.energy_per_food}}</li>
              </ul>
            </div>
          } @else {
            <div class="placeholder-content">
              <mat-icon class="large-icon">construction</mat-icon>
              <h3>Training Page Under Development</h3>
              <p>The neural network training interface is being developed.</p>
              <p>You can configure your game settings and return here to start training.</p>
            </div>
          }
        </mat-card-content>

        <mat-card-actions>
          <button mat-raised-button color="primary" (click)="goToConfig()">
            <mat-icon>settings</mat-icon>
            Configure Game
          </button>
          <button mat-button (click)="goHome()">
            <mat-icon>home</mat-icon>
            Go Home
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
    styles: [`
    .training-container {
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 80vh;
      padding: 20px;
    }

    .training-card {
      max-width: 600px;
      width: 100%;
    }

    .config-info {
      background-color: rgba(var(--mat-theme-primary-rgb), 0.05);
      padding: 16px;
      border-radius: 8px;
      margin-bottom: 16px;
    }

    .config-info h3 {
      margin: 0 0 12px 0;
      color: rgb(var(--mat-theme-primary-rgb));
    }

    .config-info ul {
      margin: 12px 0 0 0;
      padding-left: 20px;
    }

    .config-info li {
      margin-bottom: 8px;
    }

    .placeholder-content {
      text-align: center;
      padding: 32px 16px;
    }

    .large-icon {
      font-size: 64px;
      width: 64px;
      height: 64px;
      color: rgba(var(--mat-theme-on-surface-rgb), 0.5);
      margin-bottom: 16px;
    }

    .placeholder-content h3 {
      margin: 16px 0 12px 0;
      color: rgba(var(--mat-theme-on-surface-rgb), 0.7);
    }

    .placeholder-content p {
      margin: 8px 0;
      color: rgba(var(--mat-theme-on-surface-rgb), 0.6);
      line-height: 1.5;
    }

    mat-card-actions {
      display: flex;
      gap: 12px;
      justify-content: center;
    }

    mat-card-actions button mat-icon {
      margin-right: 8px;
    }

    @media (max-width: 600px) {
      .training-container {
        padding: 16px;
      }

      mat-card-actions {
        flex-direction: column;
      }

      mat-card-actions button {
        width: 100%;
      }
    }
  `]
})
export class TrainingComponent implements OnInit {
    private router = inject(Router);
    private snackBar = inject(MatSnackBar);

    gameConfig: any = null;

    ngOnInit(): void {
        // Check if game configuration was passed via router state
        const navigation = this.router.getCurrentNavigation();
        if (navigation?.extras?.state?.['gameConfig']) {
            this.gameConfig = navigation.extras.state['gameConfig'];
            this.snackBar.open('Game configuration loaded for training!', 'Close', {
                duration: 4000,
                panelClass: ['success-snackbar']
            });
        }
    }

    goToConfig(): void {
        this.router.navigate(['/config']);
    }

    goHome(): void {
        this.router.navigate(['/']);
    }
}