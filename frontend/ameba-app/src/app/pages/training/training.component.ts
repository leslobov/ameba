import { DatePipe } from '@angular/common';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { Router } from '@angular/router';
import { finalize } from 'rxjs';
import { TrainingService } from '../../services/training.service';

@Component({
  selector: 'app-training',
  standalone: true,
  imports: [
    DatePipe,
    MatButtonModule,
    MatCardModule,
    MatIconModule,
    MatSnackBarModule,
    MatFormFieldModule,
    MatInputModule,
    MatProgressSpinnerModule,
    MatCheckboxModule,
    ReactiveFormsModule
  ],
  template: `
    <div class="training-container">
      <mat-card class="training-card">
        <mat-card-header>
          <mat-icon mat-card-avatar color="accent">psychology</mat-icon>
          <mat-card-title>Neural Network Training</mat-card-title>
          <mat-card-subtitle>Train your ameba AI with evolutionary algorithms</mat-card-subtitle>
        </mat-card-header>

        <mat-card-content>
          @if (gameConfig) {
            <div class="config-info">
              <h3>Current Game Configuration</h3>
              <ul>
                <li>Game Board: {{gameConfig.play_desk.rows}}×{{gameConfig.play_desk.columns}}</li>
                <li>Neural Network Size: {{gameConfig.neural_network.initial_neurons_on_layer}} neurons</li>
                <li>Hidden Layers: {{gameConfig.neural_network.initial_hidden_layers}}</li>
                <li>Input Size: {{gameConfig.neural_network.input_size}}</li>
                <li>Energy per Food: {{gameConfig.play_desk.energy_per_food}}</li>
              </ul>
            </div>
          }

          <!-- Training Status -->
          @if (trainingStatus()) {
            <div class="status-info">
              <h3>Training Status</h3>
              <div class="status-item">
                <mat-icon [color]="trainingStatus()!.model_exists ? 'primary' : 'warn'">
                  {{trainingStatus()!.model_exists ? 'check_circle' : 'warning'}}
                </mat-icon>
                <span>Model {{trainingStatus()!.model_exists ? 'exists' : 'not found'}}</span>
              </div>
              @if (trainingStatus()!.last_modified) {
                <div class="status-item">
                  <mat-icon color="primary">schedule</mat-icon>
                  <span>Last trained: {{trainingStatus()!.last_modified | date:'medium'}}</span>
                </div>
              }
            </div>
          }

          <!-- Training Form -->
          <form [formGroup]="trainingForm" class="training-form">
            <h3>Training Parameters</h3>
            
            <div class="form-row">
              <mat-form-field appearance="outline">
                <mat-label>Training Steps</mat-label>
                <input matInput type="number" formControlName="steps" min="10" max="100000">
                <mat-hint>Number of training iterations</mat-hint>
              </mat-form-field>

              <mat-form-field appearance="outline">
                <mat-label>Batch Size</mat-label>
                <input matInput type="number" formControlName="batch_size" min="1" max="1000">
                <mat-hint>Training batch size</mat-hint>
              </mat-form-field>
            </div>

            <div class="form-row">
              <mat-checkbox formControlName="mode">
                Enable Training Mode
              </mat-checkbox>
            </div>
          </form>

          <!-- Training Result -->
          @if (trainingResult()) {
            <div class="result-info" [class.success]="trainingResult()!.success" [class.error]="!trainingResult()!.success">
              <mat-icon>{{trainingResult()!.success ? 'check_circle' : 'error'}}</mat-icon>
              <div>
                <h4>{{trainingResult()!.success ? 'Training Completed!' : 'Training Failed'}}</h4>
                <p>{{trainingResult()!.message}}</p>
                @if (trainingResult()!.steps_completed) {
                  <p><strong>Steps completed:</strong> {{trainingResult()!.steps_completed}}</p>
                }
              </div>
            </div>
          }
        </mat-card-content>

        <mat-card-actions>
          <button 
            mat-raised-button 
            color="accent" 
            (click)="startTraining()" 
            [disabled]="isTraining() || trainingForm.invalid">
            @if (isTraining()) {
              <mat-spinner diameter="20"></mat-spinner>
              Training...
            } @else {
              <ng-container>
                <mat-icon>play_arrow</mat-icon>
                Start Training
              </ng-container>
            }
          </button>

          <button mat-button (click)="refreshStatus()">
            <mat-icon>refresh</mat-icon>
            Refresh Status
          </button>

          <button mat-button (click)="goToConfig()">
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
      align-items: flex-start;
      min-height: 80vh;
      padding: 20px;
    }

    .training-card {
      max-width: 800px;
      width: 100%;
    }

    .config-info, .status-info {
      background-color: rgba(var(--mat-theme-primary-rgb), 0.05);
      padding: 16px;
      border-radius: 8px;
      margin-bottom: 16px;
    }

    .config-info h3, .status-info h3 {
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

    .status-item {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 8px;
    }

    .training-form {
      margin: 20px 0;
      padding: 16px;
      border: 1px solid rgba(var(--mat-theme-outline-rgb), 0.2);
      border-radius: 8px;
    }

    .training-form h3 {
      margin-top: 0;
      color: rgb(var(--mat-theme-primary-rgb));
    }

    .form-row {
      display: flex;
      gap: 16px;
      margin-bottom: 16px;
    }

    .form-row mat-form-field {
      flex: 1;
    }

    .result-info {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      padding: 16px;
      border-radius: 8px;
      margin: 16px 0;
    }

    .result-info.success {
      background-color: rgba(var(--mat-theme-primary-rgb), 0.1);
      border: 1px solid rgba(var(--mat-theme-primary-rgb), 0.3);
    }

    .result-info.error {
      background-color: rgba(var(--mat-theme-error-rgb), 0.1);
      border: 1px solid rgba(var(--mat-theme-error-rgb), 0.3);
    }

    .result-info h4 {
      margin: 0 0 8px 0;
    }

    .result-info p {
      margin: 4px 0;
    }

    mat-card-actions {
      display: flex;
      gap: 12px;
      justify-content: center;
      flex-wrap: wrap;
    }

    mat-card-actions button mat-icon {
      margin-right: 8px;
    }

    mat-card-actions button mat-spinner {
      margin-right: 8px;
    }

    @media (max-width: 768px) {
      .form-row {
        flex-direction: column;
      }

      mat-card-actions {
        flex-direction: column;
      }

      mat-card-actions button {
        width: 100%;
      }
    }

    @media (max-width: 600px) {
      .training-container {
        padding: 16px;
      }
    }
  `]
})
export class TrainingComponent implements OnInit {
  private router = inject(Router);
  private snackBar = inject(MatSnackBar);
  private fb = inject(FormBuilder);
  private trainingService = inject(TrainingService);

  // Signals for reactive state
  trainingStatus = signal<any>(null);
  trainingResult = signal<any>(null);
  isTraining = signal<boolean>(false);

  gameConfig: any = null;
  trainingForm: FormGroup;

  constructor() {
    // Initialize the training form
    this.trainingForm = this.fb.group({
      steps: [1000, [Validators.required, Validators.min(10), Validators.max(100000)]],
      batch_size: [32, [Validators.required, Validators.min(1), Validators.max(1000)]],
      mode: [true]
    });
  }

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

    // Load initial training status
    this.refreshStatus();
  }

  startTraining(): void {
    if (this.trainingForm.invalid || this.isTraining()) {
      return;
    }

    this.isTraining.set(true);
    this.trainingResult.set(null);

    const request = this.trainingForm.value;

    this.trainingService.startTraining(request).pipe(
      finalize(() => this.isTraining.set(false))
    ).subscribe({
      next: (response) => {
        this.trainingResult.set(response);
        if (response.success) {
          this.snackBar.open('Training completed successfully!', 'Close', {
            duration: 5000,
            panelClass: ['success-snackbar']
          });
          // Refresh status to show updated model info
          this.refreshStatus();
        } else {
          this.snackBar.open('Training failed!', 'Close', {
            duration: 5000,
            panelClass: ['error-snackbar']
          });
        }
      },
      error: (error) => {
        this.trainingResult.set({
          success: false,
          message: error.message
        });
        this.snackBar.open(`Training failed: ${error.message}`, 'Close', {
          duration: 5000,
          panelClass: ['error-snackbar']
        });
      }
    });
  }

  refreshStatus(): void {
    this.trainingService.getTrainingStatus().subscribe({
      next: (status) => {
        this.trainingStatus.set(status);
      },
      error: (error) => {
        console.error('Failed to get training status:', error);
        this.snackBar.open('Failed to get training status', 'Close', {
          duration: 3000,
          panelClass: ['error-snackbar']
        });
      }
    });
  }

  goToConfig(): void {
    this.router.navigate(['/config']);
  }

  goHome(): void {
    this.router.navigate(['/']);
  }
}