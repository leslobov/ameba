import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-about',
  imports: [MatButtonModule, MatCardModule, RouterLink],
  template: `
    <div class="about-container">
      <mat-card class="about-card">
        <mat-card-header>
          <mat-card-title>About Ameba</mat-card-title>
          <mat-card-subtitle>Learn about this project</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content class="mat-padding-v-md">
          <p>Ameba is an AI-powered simulation game where artificial organisms learn and evolve.</p>
          <p>This application demonstrates:</p>
          <ul>
            <li>Neural network AI</li>
            <li>Evolutionary algorithms</li>
            <li>Real-time simulation</li>
          </ul>
        </mat-card-content>
        <mat-card-actions class="flex-center-horizontal mat-padding-sm" style="gap: 16px;">
          <button mat-raised-button color="primary" routerLink="/">
            Back to Home
          </button>
          <button mat-stroked-button routerLink="/game">
            Start Game
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
  styles: [`
    .about-container {
      display: flex;
      justify-content: center;
      align-items: flex-start;
      min-height: 80vh;
      padding: 20px;
    }

    .about-card {
      max-width: 600px;
      width: 100%;
    }

    ul {
      margin: 16px 0;
      padding-left: 20px;
    }

    @media (max-width: 600px) {
      .about-container {
        padding: 16px;
      }
    }
  `]
})
export class AboutComponent { }