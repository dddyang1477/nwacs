import type { StyleFingerprintParams, StyleFingerprint } from '../types/index.js';

export async function extractStyleFingerprint(params: StyleFingerprintParams): Promise<StyleFingerprint> {
  try {
    const { text, action = 'extract' } = params;
    
    if (!text) {
      return { success: false, suggestions: ['请提供文本内容'] };
    }

    const features: Record<string, number> = {};
    
    features.dialogue_ratio = (text.match(/["“”]/g)?.length || 0) / text.length;
    features.description_ratio = (text.match(/的[a-zA-Z\u4e00-\u9fa5]{2,}/g)?.length || 0) / text.length;
    features.action_ratio = (text.match(/[拿提握举走跑坐站]/g)?.length || 0) / text.length;
    
    const simileCount = text.match(/像|如同|仿佛|犹如|似.*一般/g)?.length || 0;
    const hyperboleCount = text.match(/千万|亿万|无尽|滔天|毁天灭地/g)?.length || 0;
    
    const patterns: string[] = [];
    if (simileCount > 5) patterns.push('比喻丰富');
    if (hyperboleCount > 3) patterns.push('夸张手法');
    if (features.dialogue_ratio > 0.3) patterns.push('对话驱动');
    if (features.description_ratio > 0.2) patterns.push('描写细腻');

    let style_type = '标准风格';
    if (patterns.includes('比喻丰富') && patterns.includes('描写细腻')) {
      style_type = '文艺风格';
    } else if (patterns.includes('对话驱动')) {
      style_type = '剧情紧凑';
    } else if (patterns.includes('夸张手法')) {
      style_type = '热血风格';
    }

    return {
      success: true,
      features,
      style_type,
      suggestions: [
        '保持风格一致性',
        '适当增加修辞手法',
        '注意节奏变化'
      ]
    };
  } catch (error) {
    return {
      success: false,
      suggestions: [`风格分析失败: ${error instanceof Error ? error.message : String(error)}`]
    };
  }
}