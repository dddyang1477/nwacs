export async function detectAI(params) {
    try {
        const { text, detection_mode = 'standard' } = params;
        if (!text) {
            return { success: false, suggestions: ['请提供文本内容'] };
        }
        const flagged_sections = [];
        let ai_probability = 0;
        const ai_patterns = [
            /经过慎重考虑/g,
            /综上所述/g,
            /需要注意的是/g,
            /首先.*其次.*最后/g,
            /在这种情况下/g,
            /从某种意义上说/g
        ];
        ai_patterns.forEach((pattern, index) => {
            if (pattern.test(text)) {
                ai_probability += 15;
                flagged_sections.push(`检测到模板化表达: "${pattern}"`);
            }
        });
        const sentence_lengths = text.split(/[。！？]/).map(s => s.length);
        const avg_length = sentence_lengths.reduce((a, b) => a + b, 0) / sentence_lengths.length;
        if (avg_length > 50) {
            ai_probability += 10;
            flagged_sections.push('句子过长，可能为AI生成');
        }
        const unique_chars = new Set(text).size;
        if (unique_chars / text.length < 0.15) {
            ai_probability += 15;
            flagged_sections.push('词汇多样性较低');
        }
        ai_probability = Math.min(95, Math.max(5, ai_probability));
        if (detection_mode === 'deep') {
            ai_probability = Math.round(ai_probability * 0.9);
        }
        const suggestions = [];
        if (ai_probability > 60) {
            suggestions.push('建议增加个人风格表达');
            suggestions.push('使用更口语化的表达');
            suggestions.push('增加细节描写和情感表达');
        }
        else if (ai_probability > 30) {
            suggestions.push('整体质量良好，可适当增加个性化表达');
        }
        else {
            suggestions.push('AI痕迹较低，保持创作风格');
        }
        return {
            success: true,
            ai_probability,
            flagged_sections: flagged_sections.slice(0, 5),
            suggestions
        };
    }
    catch (error) {
        return {
            success: false,
            suggestions: [`AI检测失败: ${error instanceof Error ? error.message : String(error)}`]
        };
    }
}
