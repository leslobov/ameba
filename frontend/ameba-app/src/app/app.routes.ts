import { Routes } from '@angular/router';

export const routes: Routes = [
    {
        path: '',
        loadComponent: () => import('./pages/home/home.component').then(m => m.HomeComponent)
    },
    {
        path: 'about',
        loadComponent: () => import('./pages/about/about.component').then(m => m.AboutComponent)
    },
    {
        path: 'game',
        loadComponent: () => import('./pages/game/game.component').then(m => m.GameComponent)
    },
    {
        path: 'config',
        loadComponent: () => import('./pages/config/config.component').then(m => m.ConfigComponent)
    },
    {
        path: '**',
        redirectTo: ''
    }
];
