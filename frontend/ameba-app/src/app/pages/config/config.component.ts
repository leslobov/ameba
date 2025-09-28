import { Component, inject, OnInit, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatChipsModule } from '@angular/material/chips';
import { MatExpansionModule } from '@angular/material/expansion';
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

interface PlayDeskConfig {
    total_energy: number;
    energy_per_food: number;
    rows: number;
    columns: number;
}

interface AmebaConfig {
    threhold_of_lostness_weight_coefficient: number;
    visible_rows: number;
    visible_columns: number;
    initial_energy: number;
    lost_energy_per_move: number;
}

interface NeuralNetworkConfig {
    initial_hidden_layers: number;
    initial_neurons_on_layer: number;
}

interface GameConfig {
    play_desk: PlayDeskConfig;
    ameba: AmebaConfig;
    neural_network: NeuralNetworkConfig;
}

@Component({
    selector: 'app-config',
    imports: [
        ReactiveFormsModule,
        MatButtonModule,
        MatCardModule,
        MatExpansionModule,
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
    protected readonly backendConfig = signal<BackendGameConfig | null>(null);

    private readonly defaultConfig: GameConfig = {
        play_desk: {
            total_energy: 10000.0,
            energy_per_food: 50.0,
            rows: 32,
            columns: 32
        },
        ameba: {
            threhold_of_lostness_weight_coefficient: 0.2,
            visible_rows: 5,
            visible_columns: 5,
            initial_energy: 100.0,
            lost_energy_per_move: 1.0
        },
        neural_network: {
            initial_hidden_layers: 1,
            initial_neurons_on_layer: 32
        }
    };

    constructor() {
        this.configForm = this.fb.group({
            play_desk: this.fb.group({
                total_energy: [this.defaultConfig.play_desk.total_energy, [Validators.required, Validators.min(1000), Validators.max(100000)]],
                energy_per_food: [this.defaultConfig.play_desk.energy_per_food, [Validators.required, Validators.min(10), Validators.max(200)]],
                rows: [this.defaultConfig.play_desk.rows, [Validators.required, Validators.min(10), Validators.max(100)]],
                columns: [this.defaultConfig.play_desk.columns, [Validators.required, Validators.min(10), Validators.max(100)]]
            }),
            ameba: this.fb.group({
                threhold_of_lostness_weight_coefficient: [this.defaultConfig.ameba.threhold_of_lostness_weight_coefficient, [Validators.required, Validators.min(0), Validators.max(1)]],
                visible_rows: [this.defaultConfig.ameba.visible_rows, [Validators.required, Validators.min(3), Validators.max(15)]],
                visible_columns: [this.defaultConfig.ameba.visible_columns, [Validators.required, Validators.min(3), Validators.max(15)]],
                initial_energy: [this.defaultConfig.ameba.initial_energy, [Validators.required, Validators.min(50), Validators.max(500)]],
                lost_energy_per_move: [this.defaultConfig.ameba.lost_energy_per_move, [Validators.required, Validators.min(0.1), Validators.max(10)]]
            }),
            neural_network: this.fb.group({
                initial_hidden_layers: [this.defaultConfig.neural_network.initial_hidden_layers, [Validators.required, Validators.min(1), Validators.max(10)]],
                initial_neurons_on_layer: [this.defaultConfig.neural_network.initial_neurons_on_layer, [Validators.required, Validators.min(8), Validators.max(256)]]
            })
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
                this.configForm.patchValue(backendConfig);

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

        const gameConfig = this.configForm.value as GameConfig;
        this.isLoading.set(true);

        // Try to save to backend first
        this.backendApi.updateGameConfig(gameConfig).pipe(
            finalize(() => this.isLoading.set(false)),
            catchError(error => {
                console.error('Backend save failed, saving to localStorage only:', error);
                this.saveToLocalStorage(gameConfig);
                return of(null);
            })
        ).subscribe(savedConfig => {
            if (savedConfig) {
                this.backendConfig.set(savedConfig);
                this.saveToLocalStorage(gameConfig);

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
                this.configForm.patchValue(defaultConfig);

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