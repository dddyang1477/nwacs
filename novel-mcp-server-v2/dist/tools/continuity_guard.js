export async function checkContinuity(params) {
    try {
        const { check_scope = 'chapter', strictness = 'normal' } = params;
        const issues = [];
        let severity = 'low';
        const testData = {
            chapter: [
                '角色情绪转变突兀',
                '时间线不够清晰',
                '场景转换略显生硬'
            ],
            arc: [
                '伏笔回收不及时',
                '支线剧情略显拖沓',
                '节奏把控有待加强'
            ],
            full: [
                '整体结构不够紧凑',
                '部分设定前后不一致',
                '人物成长弧线有待完善'
            ]
        };
        const randomCount = strictness === 'strict' ? 3 : strictness === 'normal' ? 2 : 1;
        const availableIssues = testData[check_scope] || [];
        for (let i = 0; i < randomCount && i < availableIssues.length; i++) {
            issues.push(availableIssues[i]);
        }
        if (issues.length > 2)
            severity = 'high';
        else if (issues.length > 0)
            severity = 'medium';
        const suggestions = [];
        if (severity === 'high') {
            suggestions.push('建议全面检查设定文档');
            suggestions.push('梳理时间线和人物关系');
        }
        else if (severity === 'medium') {
            suggestions.push('建议针对性修改问题章节');
            suggestions.push('增加细节描写增强连贯性');
        }
        else {
            suggestions.push('剧情连贯性良好');
        }
        return {
            success: true,
            issues,
            severity,
            suggestions
        };
    }
    catch (error) {
        return {
            success: false,
            severity: 'low',
            suggestions: [`连贯性检查失败: ${error instanceof Error ? error.message : String(error)}`]
        };
    }
}
