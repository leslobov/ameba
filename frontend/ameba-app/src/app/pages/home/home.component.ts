import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { RouterLink } from '@angular/router';

@Component({
    selector: 'app-home',
    imports: [MatButtonModule, MatCardModule, MatIconModule, RouterLink],
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
        <mat-card-actions class="flex-center-horizontal mat-padding-sm" style="gap: 16px; flex-wrap: wrap;">
          <button mat-raised-button color="primary" routerLink="/game">
            <mat-icon>play_arrow</mat-icon>
            Start Game
          </button>
          <button mat-stroked-button routerLink="/config">
            <mat-icon>settings</mat-icon>
            Configure Game
          </button>
          <button mat-button routerLink="/about">
            <mat-icon>info</mat-icon>
            About
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