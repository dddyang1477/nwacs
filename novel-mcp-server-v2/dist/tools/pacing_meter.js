export async function analyzePacing(params) {
    try {
        const { text, chapter_position = 'rising', target_pacing = 'moderate' } = params;
        if (!text) {
            return { success: false, suggestions: ['请提供文本内容'] };
        }
        const sentences = text.split(/[。！？]/).filter(s => s.trim());
        const avg_sentence_length = sentences.reduce((sum, s) => sum + s.length, 0) / sentences.length;
        const dialogueMatches = text.match(/"[^"]*"/g) || [];
        const dialogueLength = dialogueMatches.reduce((sum, m) => sum + m.length, 0);
        const dialogue_ratio = dialogueLength / text.length;
        const action_words = text.match(/[打杀跑跳飞冲砍刺]/g)?.length || 0;
        const description_words = text.match(/的[a-zA-Z\u4e00-\u9fa5]{2,}/g)?.length || 0;
        let score = 50;
        if (target_pacing === 'fast') {
            if (avg_sentence_length < 30 && action_words > description_words) {
                score = 85 + Math.random() * 10;
            }
            else if (avg_sentence_length < 40) {
                score = 65 + Math.random() * 10;
            }
            else {
                score = 40 + Math.random() * 10;
            }
        }
        else if (target_pacing === 'moderate') {
            if (avg_sentence_length >= 30 && avg_sentence_length <= 50) {
                score = 80 + Math.random() * 10;
            }
            else {
                score = 60 + Math.random() * 15;
            }
        }
        else {
            if (avg_sentence_length > 50 && description_words > action_words) {
                score = 80 + Math.random() * 10;
            }
            else {
                score = 55 + Math.random() * 15;
            }
        }
        const issues = [];
        if (dialogue_ratio > 0.5) {
            issues.push('对话占比过高，可能影响节奏');
        }
        if (action_words === 0 && chapter_position === 'climax') {
            issues.push('高潮章节动作描写不足');
        }
        const suggestions = [];
        if (score < 60) {
            suggestions.push('建议调整句子长度');
            suggestions.push('根据章节位置调整节奏');
        }
        else if (score < 80) {
            suggestions.push('节奏基本符合预期，可适当优化');
        }
        else {
            suggestions.push('节奏把控良好');
        }
        return {
            success: true,
            score: Math.round(score),
            issues,
            suggestions
        };
    }
    catch (error) {
        return {
            success: false,
            suggestions: [`节奏分析失败: ${error instanceof Error ? error.message : String(error)}`]
        };
    }
}
