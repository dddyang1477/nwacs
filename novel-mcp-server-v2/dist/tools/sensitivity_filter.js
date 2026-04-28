export async function filterSensitivity(params) {
    try {
        const { text, check_level = 'normal', content_type = 'all' } = params;
        if (!text) {
            return { success: false, suggestions: ['请提供文本内容'] };
        }
        const sensitive_patterns = {
            violence: [/血腥|屠杀|残杀|肢解|酷刑/g],
            sexual: [/色情|裸露|挑逗|性暗示/g],
            political: [/敏感政治词汇|反动|颠覆/g],
            superstitious: [/封建迷信|邪教|巫术/g]
        };
        const sensitive_content = [];
        let risk_level = 'low';
        const types_to_check = content_type === 'all'
            ? ['violence', 'sexual', 'political', 'superstitious']
            : [content_type];
        types_to_check.forEach(type => {
            sensitive_patterns[type]?.forEach(pattern => {
                const matches = text.match(pattern);
                if (matches) {
                    sensitive_content.push(...matches.slice(0, 3));
                }
            });
        });
        if (sensitive_content.length >= 3) {
            risk_level = 'high';
        }
        else if (sensitive_content.length > 0) {
            risk_level = 'medium';
        }
        const suggestions = [];
        if (risk_level === 'high') {
            suggestions.push('检测到高风险内容，请修改');
            suggestions.push('建议使用替代词汇');
        }
        else if (risk_level === 'medium') {
            suggestions.push('检测到中等风险内容，建议审查');
        }
        else {
            suggestions.push('未检测到敏感内容');
        }
        return {
            success: true,
            sensitive_content: sensitive_content.slice(0, 5),
            risk_level,
            suggestions
        };
    }
    catch (error) {
        return {
            success: false,
            risk_level: 'low',
            suggestions: [`敏感内容检测失败: ${error instanceof Error ? error.message : String(error)}`]
        };
    }
}
