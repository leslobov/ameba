import { Component, inject, signal } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatSliderModule } from '@angular/material/slider';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';
import { RouterLink } from '@angular/router';

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
        RouterLink
    ],
    templateUrl: './config.component.html',
    styleUrl: './config.component.scss'
})
export class ConfigComponent {
    private fb = inject(FormBuilder);
    private snackBar = inject(MatSnackBar);

    protected readonly configForm: FormGroup;
    protected readonly previewData = signal<GameConfig | null>(null);

    private readonly defaultConfig: GameConfig = {
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

        // Load saved configuration if available
        this.loadSavedConfig();
    }

    protected saveConfig(): void {
        if (this.configForm.valid) {
            const config = this.configForm.value as GameConfig;

            // Save to localStorage
            localStorage.setItem('amebaGameConfig', JSON.stringify(config));

            this.snackBar.open('Configuration saved successfully!', 'Close', {
                duration: 3000,
                panelClass: ['success-snackbar']
            });

            console.log('Saved configuration:', config);
        } else {
            this.snackBar.open('Please fix validation errors before saving.', 'Close', {
                duration: 3000,
                panelClass: ['error-snackbar']
            });
        }
    }

    protected resetToDefaults(): void {
        this.configForm.patchValue(this.defaultConfig);
        this.snackBar.open('Configuration reset to defaults', 'Close', {
            duration: 2000
        });
    }

    protected previewConfig(): void {
        if (this.configForm.valid) {
            const config = this.configForm.value as GameConfig;
            this.previewData.set(config);

            this.snackBar.open('Preview updated! Check browser console for details.', 'Close', {
                duration: 3000
            });

            console.log('Configuration Preview:', config);
        }
    }

    private loadSavedConfig(): void {
        const saved = localStorage.getItem('amebaGameConfig');
        if (saved) {
            try {
                const config = JSON.parse(saved) as GameConfig;
                this.configForm.patchValue(config);
            } catch (error) {
                console.warn('Failed to load saved configuration:', error);
            }
        }
    }
}