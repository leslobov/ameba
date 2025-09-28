import { Injectable, signal } from '@angular/core';

export interface GameConfig {
    worldWidth: number;
    worldHeight: number;
    initialAmebaCount: number;
    initialFoodCount: number;
    maxSimulationSpeed: number;
    energyDecayRate: number;
    reproductionThreshold: number;
    mutationRate: number;
    enableNeuralNetwork: boolean;
    networkComplexity: 'simple' | 'medium' | 'complex';
    autoSave: boolean;
}

@Injectable({
    providedIn: 'root'
})
export class GameConfigService {
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

    private readonly configSignal = signal<GameConfig>(this.defaultConfig);

    // Public readonly signal for components to consume
    public readonly config = this.configSignal.asReadonly();

    constructor() {
        this.loadConfigFromStorage();
    }

    /**
     * Update the game configuration
     */
    updateConfig(newConfig: Partial<GameConfig>): void {
        const updatedConfig = { ...this.configSignal(), ...newConfig };
        this.configSignal.set(updatedConfig);

        if (updatedConfig.autoSave) {
            this.saveConfigToStorage(updatedConfig);
        }
    }

    /**
     * Reset configuration to defaults
     */
    resetToDefaults(): void {
        this.configSignal.set(this.defaultConfig);
        this.saveConfigToStorage(this.defaultConfig);
    }

    /**
     * Save current configuration to localStorage
     */
    saveCurrentConfig(): void {
        this.saveConfigToStorage(this.configSignal());
    }

    /**
     * Load configuration from localStorage
     */
    loadConfigFromStorage(): void {
        try {
            const saved = localStorage.getItem('amebaGameConfig');
            if (saved) {
                const parsedConfig = JSON.parse(saved) as GameConfig;

                // Validate the loaded config has all required properties
                const validatedConfig = { ...this.defaultConfig, ...parsedConfig };
                this.configSignal.set(validatedConfig);
            }
        } catch (error) {
            console.warn('Failed to load game configuration from storage:', error);
            this.configSignal.set(this.defaultConfig);
        }
    }

    /**
     * Get configuration for specific game aspects
     */
    getWorldSettings() {
        const config = this.configSignal();
        return {
            width: config.worldWidth,
            height: config.worldHeight
        };
    }

    getPopulationSettings() {
        const config = this.configSignal();
        return {
            amebaCount: config.initialAmebaCount,
            foodCount: config.initialFoodCount
        };
    }

    getSimulationSettings() {
        const config = this.configSignal();
        return {
            speed: config.maxSimulationSpeed,
            energyDecay: config.energyDecayRate,
            reproductionThreshold: config.reproductionThreshold
        };
    }

    getAISettings() {
        const config = this.configSignal();
        return {
            enabled: config.enableNeuralNetwork,
            complexity: config.networkComplexity,
            mutationRate: config.mutationRate
        };
    }

    /**
     * Export configuration as JSON for sharing/backup
     */
    exportConfig(): string {
        return JSON.stringify(this.configSignal(), null, 2);
    }

    /**
     * Import configuration from JSON string
     */
    importConfig(configJson: string): boolean {
        try {
            const importedConfig = JSON.parse(configJson) as GameConfig;

            // Validate imported config
            const validatedConfig = { ...this.defaultConfig, ...importedConfig };
            this.configSignal.set(validatedConfig);
            this.saveConfigToStorage(validatedConfig);

            return true;
        } catch (error) {
            console.error('Failed to import configuration:', error);
            return false;
        }
    }

    private saveConfigToStorage(config: GameConfig): void {
        try {
            localStorage.setItem('amebaGameConfig', JSON.stringify(config));
        } catch (error) {
            console.warn('Failed to save game configuration to storage:', error);
        }
    }
}