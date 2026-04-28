import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { CallToolRequestSchema, ListToolsRequestSchema } from '@modelcontextprotocol/sdk/types.js';
import { analyzeTrend } from './tools/trend_analyzer.js';
import { operateWorld } from './tools/world_builder.js';
import { extractStyleFingerprint } from './tools/style_fingerprint.js';
import { detectAI } from './tools/ai_detector.js';
import { checkContinuity } from './tools/continuity_guard.js';
import { analyzePacing } from './tools/pacing_meter.js';
import { tuneDialogue } from './tools/dialogue_tuner.js';
import { filterSensitivity } from './tools/sensitivity_filter.js';
import { simulateReader } from './tools/reader_simulator.js';
import { enhanceVisualization } from './tools/scene_visualizer.js';
const server = new Server({
    name: 'novel-creation-server',
    version: '1.1.0'
}, {
    capabilities: {
        tools: {}
    }
});
const TOOLS = [
    {
        name: 'trend_analyzer',
        description: '分析小说市场趋势，提供创作建议',
        inputSchema: {
            type: 'object',
            properties: {
                platform: { type: 'string', enum: ['qidian', 'fanqie', 'qimao', 'jjwxc', 'zhihu', 'wechat'] },
                genre: { type: 'string', enum: ['xuanhuan', 'wuxia', 'urban', 'sci-fi', 'mystery', 'romance', 'history'] },
                time_range: { type: 'string', enum: ['week', 'month', 'quarter'], default: 'month' }
            },
            required: ['platform', 'genre']
        }
    },
    {
        name: 'world_builder',
        description: '构建和管理小说世界观',
        inputSchema: {
            type: 'object',
            properties: {
                action: { type: 'string', enum: ['create', 'query', 'validate', 'expand'] },
                novel_id: { type: 'string' },
                content: { type: 'string' },
                dimension: { type: 'string', enum: ['geography', 'power_system', 'history', 'faction', 'culture'] }
            },
            required: ['action', 'novel_id']
        }
    },
    {
        name: 'style_fingerprint',
        description: '提取和分析作者风格指纹',
        inputSchema: {
            type: 'object',
            properties: {
                text: { type: 'string' },
                action: { type: 'string', enum: ['extract', 'compare', 'adapt'], default: 'extract' },
                target_text: { type: 'string' },
                target_genre: { type: 'string' }
            },
            required: ['text']
        }
    },
    {
        name: 'ai_detector',
        description: '检测文本AI痕迹并提供优化建议',
        inputSchema: {
            type: 'object',
            properties: {
                text: { type: 'string' },
                detection_mode: { type: 'string', enum: ['standard', 'deep'], default: 'standard' },
                focus_areas: { type: 'array', items: { type: 'string' } }
            },
            required: ['text']
        }
    },
    {
        name: 'continuity_guard',
        description: '检查剧情连贯性和一致性',
        inputSchema: {
            type: 'object',
            properties: {
                novel_id: { type: 'string' },
                check_scope: { type: 'string', enum: ['chapter', 'arc', 'full'], default: 'chapter' },
                strictness: { type: 'string', enum: ['loose', 'normal', 'strict'], default: 'normal' }
            },
            required: ['novel_id']
        }
    },
    {
        name: 'pacing_meter',
        description: '分析章节节奏和阅读体验',
        inputSchema: {
            type: 'object',
            properties: {
                text: { type: 'string' },
                chapter_position: { type: 'string', enum: ['opening', 'rising', 'climax', 'falling', 'ending'] },
                target_pacing: { type: 'string', enum: ['fast', 'moderate', 'slow'], default: 'moderate' }
            },
            required: ['text']
        }
    },
    {
        name: 'dialogue_tuner',
        description: '优化对话自然度和角色区分度',
        inputSchema: {
            type: 'object',
            properties: {
                dialogue: { type: 'string' },
                characters: { type: 'array', items: { type: 'string' } },
                scene_context: { type: 'string' },
                tune_mode: { type: 'string', enum: ['natural', 'characteristic', 'dramatic'], default: 'natural' }
            },
            required: ['dialogue']
        }
    },
    {
        name: 'sensitivity_filter',
        description: '检测和过滤敏感内容',
        inputSchema: {
            type: 'object',
            properties: {
                text: { type: 'string' },
                check_level: { type: 'string', enum: ['strict', 'normal', 'loose'], default: 'normal' },
                content_type: { type: 'string', enum: ['violence', 'sexual', 'political', 'superstitious', 'all'], default: 'all' }
            },
            required: ['text']
        }
    },
    {
        name: 'reader_simulator',
        description: '模拟读者反应和阅读体验',
        inputSchema: {
            type: 'object',
            properties: {
                text: { type: 'string' },
                reader_group: { type: 'string', enum: ['teen_male', 'young_male', 'young_female', 'mature_male', 'mature_female'] },
                simulation_depth: { type: 'string', enum: ['surface', 'deep'], default: 'surface' }
            },
            required: ['text']
        }
    },
    {
        name: 'scene_visualizer',
        description: '增强场景画面感和影视化效果',
        inputSchema: {
            type: 'object',
            properties: {
                text: { type: 'string' },
                genre: { type: 'string', enum: ['xuanhuan', 'wuxia', 'urban', 'sci-fi', 'mystery', 'romance', 'history'] },
                enhancement_level: { type: 'string', enum: ['light', 'standard', 'deep'], default: 'standard' },
                target_senses: { type: 'array', items: { type: 'string', enum: ['visual', 'auditory', 'tactile', 'olfactory', 'gustatory'] }, default: ['visual', 'auditory', 'tactile'] },
                use_shot_language: { type: 'boolean', default: true }
            },
            required: ['text', 'genre']
        }
    }
];
server.setRequestHandler(ListToolsRequestSchema, async () => {
    return { tools: TOOLS };
});
server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name, arguments: args } = request.params;
    try {
        let result;
        switch (name) {
            case 'trend_analyzer':
                result = await analyzeTrend(args);
                break;
            case 'world_builder':
                result = await operateWorld(args);
                break;
            case 'style_fingerprint':
                result = await extractStyleFingerprint(args);
                break;
            case 'ai_detector':
                result = await detectAI(args);
                break;
            case 'continuity_guard':
                result = await checkContinuity(args);
                break;
            case 'pacing_meter':
                result = await analyzePacing(args);
                break;
            case 'dialogue_tuner':
                result = await tuneDialogue(args);
                break;
            case 'sensitivity_filter':
                result = await filterSensitivity(args);
                break;
            case 'reader_simulator':
                result = await simulateReader(args);
                break;
            case 'scene_visualizer':
                result = await enhanceVisualization(args);
                break;
            default:
                result = { success: false, error: `未知工具: ${name}` };
        }
        return { content: [{ type: 'text', text: JSON.stringify(result) }] };
    }
    catch (error) {
        const errorResult = { success: false, error: `工具执行错误: ${error instanceof Error ? error.message : String(error)}` };
        return { content: [{ type: 'text', text: JSON.stringify(errorResult) }], isError: true };
    }
});
export async function startServer() {
    const transport = new StdioServerTransport();
    await server.connect(transport);
    console.error('Novel Creation MCP Server v1.1.0 running on stdio');
}
startServer().catch(console.error);
