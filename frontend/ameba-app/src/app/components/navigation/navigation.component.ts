import { Component } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatToolbarModule } from '@angular/material/toolbar';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
    selector: 'app-navigation',
    imports: [MatToolbarModule, MatButtonModule, MatIconModule, RouterLink, RouterLinkActive],
    template: `
    <mat-toolbar color="primary">
      <mat-toolbar-row>
        <span class="app-title">
          <mat-icon>biotech</mat-icon>
          Ameba AI
        </span>
        
        <span class="spacer"></span>
        
        <nav class="nav-links">
          <button mat-button routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">
            <mat-icon>home</mat-icon>
            Home
          </button>
          <button mat-button routerLink="/about" routerLinkActive="active">
            <mat-icon>info</mat-icon>
            About
          </button>
          <button mat-button routerLink="/game" routerLinkActive="active">
            <mat-icon>videogame_asset</mat-icon>
            Game
          </button>
          <button mat-button routerLink="/config" routerLinkActive="active">
            <mat-icon>settings</mat-icon>
            Config
          </button>
        </nav>
      </mat-toolbar-row>
    </mat-toolbar>
  `,
    styles: [`
    .app-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-weight: 500;
    }
    
    .spacer {
      flex: 1 1 auto;
    }
    
    .nav-links {
      display: flex;
      gap: 8px;
    }
    
    .nav-links button {
      display: flex;
      align-items: center;
      gap: 4px;
    }
    
    .nav-links button.active {
      background-color: rgba(255, 255, 255, 0.1);
    }
    
    @media (max-width: 768px) {
      .nav-links button span {
        display: none;
      }
    }
  `]
})
export class NavigationComponent { }