import { Component, inject } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatIconModule } from '@angular/material/icon';

@Component({
    selector: 'app-training-confirm-dialog',
    standalone: true,
    imports: [
        MatDialogModule,
        MatButtonModule,
        MatIconModule
    ],
    template: `
    <div class="dialog-container">
      <h2 mat-dialog-title class="dialog-title">
        <mat-icon color="accent">psychology</mat-icon>
        Train Neural Network?
      </h2>
      
      <div mat-dialog-content class="dialog-content">
        <p>Your game configuration has been saved successfully!</p>
        <p>Would you like to start training the neural network with this new configuration?</p>
        
        <div class="info-box">
          <mat-icon>info</mat-icon>
          <span>This will create a new training run using your current game settings.</span>
        </div>
      </div>
      
      <div mat-dialog-actions class="dialog-actions">
        <button mat-button (click)="onCancel()" class="cancel-button">
          <mat-icon>close</mat-icon>
          Not Now
        </button>
        <button mat-raised-button color="accent" (click)="onConfirm()" class="confirm-button">
          <mat-icon>play_arrow</mat-icon>
          Start Training
        </button>
      </div>
    </div>
  `,
    styles: [`
    .dialog-container {
      padding: 0;
      min-width: 400px;
      max-width: 500px;
    }

    .dialog-title {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 0;
      padding: 24px 24px 16px 24px;
      font-size: 1.5rem;
      font-weight: 500;
    }

    .dialog-content {
      padding: 0 24px 16px 24px;
      line-height: 1.6;
    }

    .dialog-content p {
      margin: 0 0 16px 0;
    }

    .dialog-content p:last-of-type {
      margin-bottom: 24px;
    }

    .info-box {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 16px;
      background-color: rgba(var(--mat-theme-primary-rgb), 0.08);
      border-radius: 8px;
      border-left: 4px solid rgb(var(--mat-theme-primary-rgb));
      font-size: 0.9rem;
    }

    .info-box mat-icon {
      color: rgb(var(--mat-theme-primary-rgb));
      font-size: 20px;
      width: 20px;
      height: 20px;
    }

    .dialog-actions {
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      padding: 16px 24px 24px 24px;
      margin: 0;
    }

    .cancel-button {
      color: rgba(var(--mat-theme-on-surface-rgb), 0.7);
    }

    .confirm-button {
      min-width: 140px;
    }

    .cancel-button mat-icon,
    .confirm-button mat-icon {
      margin-right: 8px;
      font-size: 18px;
      width: 18px;
      height: 18px;
    }

    @media (max-width: 500px) {
      .dialog-container {
        min-width: 300px;
        max-width: 90vw;
      }

      .dialog-actions {
        flex-direction: column-reverse;
        gap: 8px;
      }

      .cancel-button,
      .confirm-button {
        width: 100%;
      }
    }
  `]
})
export class TrainingConfirmDialogComponent {
    private dialogRef = inject(MatDialogRef<TrainingConfirmDialogComponent>);

    onConfirm(): void {
        this.dialogRef.close(true);
    }

    onCancel(): void {
        this.dialogRef.close(false);
    }
}