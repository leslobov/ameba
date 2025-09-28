import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { RouterLink } from '@angular/router';

@Component({
    selector: 'app-home',
    imports: [MatButtonModule, MatCardModule, RouterLink],
    template: `
    <div class="flex-center mat-padding-lg">
      <mat-card class="mat-card-center">
        <mat-card-header>
          <mat-card-title>Welcome Home!</mat-card-title>
          <mat-card-subtitle>This is the home page</mat-card-subtitle>
        </mat-card-header>
        <mat-card-content class="mat-padding-v-md">
          <p>Welcome to the Ameba application. Navigate using the buttons below:</p>
        </mat-card-content>
        <mat-card-actions class="flex-center-horizontal mat-padding-sm" style="gap: 16px;">
          <button mat-raised-button color="primary" routerLink="/about">
            Go to About
          </button>
          <button mat-stroked-button routerLink="/game">
            Start Game
          </button>
        </mat-card-actions>
      </mat-card>
    </div>
  `,
    styles: [`
    mat-card {
      max-width: 500px;
    }
  `]
})
export class HomeComponent { }