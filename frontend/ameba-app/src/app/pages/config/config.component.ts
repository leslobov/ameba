import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { RouterLink } from '@angular/router';
import { catchError, finalize, of } from 'rxjs';
import { BackendApiService, BackendGameConfig } from '../../services/backend-api.service';

interface GameConfig {
    worldWidth: number;
    worldHeight: number;
    initialAmebaCount: number;
    initialFoodCount: number;
    maxSimulationSpeed: number;
    energyDecayRate: number;
    reproductionThreshold: number;
    mutationRate: number;
    enableNeuralNetwork: boolean;
    networkComplexity: string;
    autoSave: boolean;
}

@Component({
    selector: 'app-config',
    imports: [
        ReactiveFormsModule,
        MatButtonModule,
        MatCardModule,
        MatFormFieldModule,
        MatInputModule,
        MatSliderModule,
        MatSelectModule,
        MatCheckboxModule,
        MatIconModule,
        MatSnackBarModule,
        MatProgressSpinnerModule,
        MatChipsModule,
        RouterLink
    ],
    templateUrl: './config.component.html',
    styleUrl: './config.component.scss'
})
export class ConfigComponent implements OnInit {
    private fb = inject(FormBuilder);
    private snackBar = inject(MatSnackBar);
    private backendApi = inject(BackendApiService);

    protected readonly configForm: FormGroup;
    protected readonly previewData = signal<GameConfig | null>(null);
    protected readonly isLoading = signal<boolean>(false);
    protected readonly backendConfig = signal<BackendGameConfig | null>(null); private readonly defaultConfig: GameConfig = {
        worldWidth: 800,
        worldHeight: 600,
        initialAmebaCount: 20,
        initialFoodCount: 100,
        maxSimulationSpeed: 3,
        energyDecayRate: 1.0,
        reproductionThreshold: 100,
        mutationRate: 0.1,
        enableNeuralNetwork: true,
        networkComplexity: 'medium',
        autoSave: true
    };

    constructor() {
        this.configForm = this.fb.group({
            worldWidth: [this.defaultConfig.worldWidth, [Validators.required, Validators.min(50), Validators.max(1000)]],
            worldHeight: [this.defaultConfig.worldHeight, [Validators.required, Validators.min(50), Validators.max(1000)]],
            initialAmebaCount: [this.defaultConfig.initialAmebaCount, [Validators.required, Validators.min(1), Validators.max(100)]],
            initialFoodCount: [this.defaultConfig.initialFoodCount, [Validators.required, Validators.min(10), Validators.max(500)]],
            maxSimulationSpeed: [this.defaultConfig.maxSimulationSpeed, [Validators.required, Validators.min(1), Validators.max(10)]],
            energyDecayRate: [this.defaultConfig.energyDecayRate, [Validators.required, Validators.min(0.1), Validators.max(5)]],
            reproductionThreshold: [this.defaultConfig.reproductionThreshold, [Validators.required, Validators.min(50), Validators.max(200)]],
            mutationRate: [this.defaultConfig.mutationRate, [Validators.required, Validators.min(0.01), Validators.max(0.5)]],
            enableNeuralNetwork: [this.defaultConfig.enableNeuralNetwork],
            networkComplexity: [this.defaultConfig.networkComplexity, Validators.required],
            autoSave: [this.defaultConfig.autoSave]
        });
    }

    ngOnInit(): void {
        // Load configuration from backend on component initialization
        this.loadConfigFromBackend();
    }

    /**
     * Load configuration from backend API
     */
    protected loadConfigFromBackend(): void {
        this.isLoading.set(true);

        this.backendApi.getGameConfig().pipe(
            finalize(() => this.isLoading.set(false)),
            catchError(error => {
                console.warn('Failed to load backend config, using localStorage fallback:', error);
                this.loadSavedConfig();
                return of(null);
            })
        ).subscribe(backendConfig => {
            if (backendConfig) {
                this.backendConfig.set(backendConfig);
                const frontendConfig = this.backendApi.mapBackendToFrontend(backendConfig);
                this.configForm.patchValue(frontendConfig);

                this.snackBar.open('Configuration loaded from server', 'Close', {
                    duration: 2000,
                    panelClass: ['success-snackbar']
                });
            }
        });
    }

    /**
     * Save configuration to backend API and localStorage
     */
    protected saveConfig(): void {
        if (!this.configForm.valid) {
            this.snackBar.open('Please fix validation errors before saving.', 'Close', {
                duration: 3000,
                panelClass: ['error-snackbar']
            });
            return;
        }

        const frontendConfig = this.configForm.value as GameConfig;
        this.isLoading.set(true);

        // Always try to save to backend first
        const backendConfig = this.backendApi.mapFrontendToBackend(frontendConfig);

        this.backendApi.updateGameConfig(backendConfig).pipe(
            finalize(() => this.isLoading.set(false)),
            catchError(error => {
                console.error('Backend save failed, saving to localStorage only:', error);
                this.saveToLocalStorage(frontendConfig);
                return of(null);
            })
        ).subscribe(savedConfig => {
            if (savedConfig) {
                this.backendConfig.set(savedConfig);
                this.saveToLocalStorage(frontendConfig);

                this.snackBar.open('Configuration saved to server and locally!', 'Close', {
                    duration: 3000,
                    panelClass: ['success-snackbar']
                });
            }
        });
    }

    /**
     * Reset configuration to defaults (backend + frontend)
     */
    protected resetToDefaults(): void {
        this.isLoading.set(true);

        // Always try to reset backend to defaults first
        this.backendApi.resetConfigToDefaults().pipe(
            finalize(() => this.isLoading.set(false)),
            catchError(error => {
                console.error('Backend reset failed:', error);
                this.resetToLocalDefaults();
                return of(null);
            })
        ).subscribe(defaultConfig => {
            if (defaultConfig) {
                this.backendConfig.set(defaultConfig);
                const frontendConfig = this.backendApi.mapBackendToFrontend(defaultConfig);
                this.configForm.patchValue(frontendConfig);

                this.snackBar.open('Configuration reset to defaults on server and locally', 'Close', {
                    duration: 3000,
                    panelClass: ['success-snackbar']
                });
            }
        });
    }

    /**
     * Preview current configuration
     */
    protected previewConfig(): void {
        if (this.configForm.valid) {
            const config = this.configForm.value as GameConfig;
            this.previewData.set(config);

            this.snackBar.open('Preview updated! Check browser console for details.', 'Close', {
                duration: 3000
            });

            console.log('Configuration Preview:', config);

            if (this.backendConfig()) {
                console.log('Current Backend Config:', this.backendConfig());
                console.log('Mapped Frontend Config:', this.backendApi.mapBackendToFrontend(this.backendConfig()!));
            }
        }
    }



    /**
     * Save configuration to localStorage only
     */
    private saveToLocalStorage(config: GameConfig): void {
        try {
            localStorage.setItem('amebaGameConfig', JSON.stringify(config));

            this.snackBar.open('Configuration saved locally', 'Close', {
                duration: 3000,
                panelClass: ['success-snackbar']
            });
        } catch (error) {
            console.error('Failed to save to localStorage:', error);
            this.snackBar.open('Failed to save configuration', 'Close', {
                duration: 3000,
                panelClass: ['error-snackbar']
            });
        }
    }

    /**
     * Reset to local defaults only
     */
    private resetToLocalDefaults(): void {
        this.configForm.patchValue(this.defaultConfig);
        this.snackBar.open('Configuration reset to defaults locally', 'Close', {
            duration: 2000,
            panelClass: ['warning-snackbar']
        });
    }

    /**
     * Load configuration from localStorage (fallback)
     */
    private loadSavedConfig(): void {
        const saved = localStorage.getItem('amebaGameConfig');
        if (saved) {
            try {
                const config = JSON.parse(saved) as GameConfig;
                this.configForm.patchValue(config);

                this.snackBar.open('Configuration loaded from local storage', 'Close', {
                    duration: 2000,
                    panelClass: ['info-snackbar']
                });
            } catch (error) {
                console.warn('Failed to load saved configuration:', error);
                this.configForm.patchValue(this.defaultConfig);
            }
        } else {
            this.configForm.patchValue(this.defaultConfig);
        }
    }
}