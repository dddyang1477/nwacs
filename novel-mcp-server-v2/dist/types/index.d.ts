export type Genre = 'xuanhuan' | 'wuxia' | 'urban' | 'sci-fi' | 'mystery' | 'romance' | 'history';
export type Platform = 'qidian' | 'fanqie' | 'qimao' | 'jjwxc' | 'zhihu' | 'wechat';
export type ChapterPosition = 'opening' | 'rising' | 'climax' | 'falling' | 'ending';
export type CheckScope = 'chapter' | 'arc' | 'full';
export type Strictness = 'loose' | 'normal' | 'strict';
export type ReaderGroup = 'teen_male' | 'young_male' | 'young_female' | 'mature_male' | 'mature_female';
export interface TrendAnalyzerParams {
    platform: Platform;
    genre: Genre;
    time_range?: 'week' | 'month' | 'quarter';
}
export interface WorldBuilderParams {
    action: 'create' | 'query' | 'validate' | 'expand';
    novel_id: string;
    content?: string;
    dimension?: 'geography' | 'power_system' | 'history' | 'faction' | 'culture';
}
export interface StyleFingerprintParams {
    text: string;
    action?: 'extract' | 'compare' | 'adapt';
    target_text?: string;
    target_genre?: string;
}
export interface AIDetectionParams {
    text: string;
    detection_mode?: 'standard' | 'deep';
    focus_areas?: string[];
}
export interface ContinuityCheckParams {
    novel_id: string;
    check_scope?: 'chapter' | 'arc' | 'full';
    strictness?: 'loose' | 'normal' | 'strict';
}
export interface PacingAnalysisParams {
    text: string;
    chapter_position?: ChapterPosition;
    target_pacing?: 'fast' | 'moderate' | 'slow';
}
export interface DialogueTunerParams {
    dialogue: string;
    characters?: string[];
    scene_context?: string;
    tune_mode?: 'natural' | 'characteristic' | 'dramatic';
}
export interface SensitivityFilterParams {
    text: string;
    check_level?: 'strict' | 'normal' | 'loose';
    content_type?: 'violence' | 'sexual' | 'political' | 'superstitious' | 'all';
}
export interface ReaderSimulatorParams {
    text: string;
    reader_group?: ReaderGroup;
    simulation_depth?: 'surface' | 'deep';
}
export interface SceneVisualizerParams {
    text: string;
    genre: Genre;
    enhancement_level?: 'light' | 'standard' | 'deep';
    target_senses?: ('visual' | 'auditory' | 'tactile' | 'olfactory' | 'gustatory')[];
    use_shot_language?: boolean;
}
export interface TrendAnalysisResult {
    success: boolean;
    hot_topics?: string[];
    rising_authors?: string[];
    recommendations?: string[];
    market_data?: Record<string, number | string>;
}
export interface WorldBuilderResult {
    success: boolean;
    world_data?: Record<string, any>;
    contradictions?: string[];
    suggestions?: string[];
}
export interface StyleFingerprint {
    success: boolean;
    features?: Record<string, number>;
    style_type?: string;
    suggestions?: string[];
}
export interface AIDetectionResult {
    success: boolean;
    ai_probability?: number;
    flagged_sections?: string[];
    suggestions?: string[];
}
export interface ContinuityReport {
    success: boolean;
    issues?: string[];
    severity?: 'low' | 'medium' | 'high';
    suggestions?: string[];
}
export interface PacingAnalysis {
    success: boolean;
    score?: number;
    issues?: string[];
    suggestions?: string[];
}
export interface DialogueAnalysis {
    success: boolean;
    naturalness_score?: number;
    character_consistency?: Record<string, number>;
    suggestions?: string[];
}
export interface SensitivityReport {
    success: boolean;
    sensitive_content?: string[];
    risk_level?: 'low' | 'medium' | 'high';
    suggestions?: string[];
}
export interface ReaderSimulation {
    success: boolean;
    engagement_score?: number;
    predicted_drop_points?: number[];
    suggestions?: string[];
}
export interface SceneVisualization {
    success: boolean;
    enhanced_text?: string;
    shot_list?: string[];
    suggestions?: string[];
}
export type ToolResult<T> = T & {
    success: boolean;
};
