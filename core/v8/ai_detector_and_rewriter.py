#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
【NWACS AI去痕与检测模块】
📋 功能：
1. AI检测 - 识别AI写作特征
2. AI去痕 - 自动重写，去除AI痕迹
3. 增强 - 提升人类化特征
"""

import re
import random

class AIDetectorAndRewriter:
    """AI检测与去痕类"""
    
    def __init__(self):
        # AI写作特征词库
        self.ai_indicators = [
            "宛如", "仿佛", "似乎", "犹如", "宛若", "恰似",
            "不禁", "不由得", "忍不住",
            "非常", "极其", "极为", "十分", "特别", "格外",
            "缓缓地", "慢慢地", "渐渐地", "轻轻地", "悄悄地",
            "地动山摇", "天翻地覆", "海枯石烂",
            "微微一笑", "轻轻一笑", "淡淡一笑",
            "心中暗想", "心中思索", "心中暗忖"
        ]
        
        # AI句式特征
        self.ai_patterns = [
            (r"^(虽然|尽管|即使).*(，|。)", 0.3),  # 转折句开头频率过高
            (r"[！？]{2,}", 0.4),  # 连续标点符号
            (r"\.{4,}", 0.3),  # 长省略号
            (r"，.*，.*，.*，", 0.2),  # 逗号密集
        ]
    
    def detect_ai_score(self, text):
        """检测AI写作分数 - 0-100分，越高越像AI"""
        score = 0
        
        # 1. 特征词检测
        word_hits = 0
        for word in self.ai_indicators:
            word_hits += text.count(word)
        
        score += min(word_hits * 3, 40)
        
        # 2. 句式检测
        pattern_hits = 0
        for pattern, weight in self.ai_patterns:
            matches = re.findall(pattern, text)
            pattern_hits += len(matches) * weight * 10
        
        score += min(int(pattern_hits), 30)
        
        # 3. 段落检测
        lines = text.split('\n')
        if len(lines) > 5:
            # 检查是否开头结构类似
            similar_starts = 0
            for i in range(1, min(len(lines), 15)):
                if lines[i].startswith(('他', '她', '它', '这', '那')) and lines[i-1].startswith(('他', '她', '它', '这', '那')):
                    similar_starts +=1
            
            score += min(similar_starts * 5, 30)
        
        return min(score, 100)
    
    def rewrite_remove_ai(self, text):
        """重写去除AI痕迹 - 核心函数"""
        result = text
        
        # 1. 替换特征词
        replacements = {
            "宛如": "像",
            "仿佛": "好像",
            "似乎": "仿佛",
            "犹如": "像",
            "宛若": "好似",
            "恰似": "就像",
            "不禁": "忍不住",
            "不由得": "不自觉地",
            "非常": "很",
            "极其": "特别",
            "极为": "非常",
            "十分": "很",
            "特别": "非常",
            "格外": "特别",
            "缓缓地": "慢慢",
            "慢慢地": "缓缓",
            "渐渐地": "逐步",
            "轻轻地": "轻轻",
            "悄悄地": "悄悄",
            "微微一笑": "笑了笑",
            "轻轻一笑": "轻轻一笑",
            "淡淡一笑": "微微笑了笑"
        }
        
        for old, new in replacements.items():
            result = result.replace(old, new)
        
        # 2. 随机增删变换
        # 添加一些小的口语化或瑕疵（增加人味）
        humanizers = [
            "，嗯，",
            "——",
            "……",
            "？",
            "！"
        ]
        
        # 随机变换标点
        lines = result.split('。')
        new_lines = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            words = list(line)
            if random.random() < 0.15:
                if len(words) > 10:
                    idx = random.randint(3, len(words)-3)
                    if random.random() < 0.5:
                        words.insert(idx, "呢" if "？" in line else "呢")
            
            new_line = ''.join(words) if len(line) > 10 else line
            new_lines.append(new_line + "。")
        
        result = ''.join(new_lines)
        
        # 3. 段落重排，打乱完美整齐的结构
        result = self._shuffle_paragraphs(result)
        
        return result
    
    def _shuffle_paragraphs(self, text):
        """段落打乱 - 增加自然度"""
        paras = text.split('\n\n')
        
        if len(paras) < 3:
            return text
        
        # 保持开头和结尾不动，中间部分随机化
        new_paras = [paras[0]]
        
        for para in paras[1:-1]:
            # 有概率拆分段落
            if len(para) > 400 and random.random() < 0.3:
                mid = len(para) // 2
                part1, part2 = para[:mid], para[mid:]
                new_paras.extend([part1, part2])
            else:
                new_paras.append(para)
        
        new_paras.append(paras[-1])
        
        return '\n\n'.join(new_paras)
    
    def enhance_humanize(self, text):
        """增强人类化特征"""
        result = text
        
        # 1. 增加一些小的语气词
        modal_words = ["嗯", "哦", "呢", "吧", "嘛"]
        for word in modal_words:
            # 每500字随机插入一次
            if random.random() < 0.2:
                idx = result.find("。", random.randint(0, len(result)-10))
                if idx > 0:
                    result = result[:idx] + f"{word}。" + result[idx+1:]
        
        # 2. 增加重复词或不完美表达
        imperfection = ["等等", "之类的", "之类", "什么的", "有点", "比较"]
        for word in imperfection:
            if random.random() < 0.1:
                if "，" in result:
                    pos = result.find("，", len(result)//2)
                    if pos > 0:
                        result = result[:pos] + f"，{word}" + result[pos:]
        
        return result
    
    def check_and_rewrite(self, text):
        """完整检测-重写流程"""
        print("\n" + "="*60)
        print("🔍 AI检测与去痕")
        print("="*60)
        
        # 1. 初始检测
        original_score = self.detect_ai_score(text)
        print(f"📊 初始AI分数: {original_score}/100")
        
        if original_score < 30:
            print("✅ AI痕迹很少，无需重写")
            return text
        
        # 2. 需要重写
        print("⚙️ 正在去痕重写...")
        
        rewritten = self.rewrite_remove_ai(text)
        rewritten = self.enhance_humanize(rewritten)
        
        final_score = self.detect_ai_score(rewritten)
        print(f"📊 去痕后分数: {final_score}/100")
        
        reduction = original_score - final_score
        print(f"✨ 降低: {reduction}分")
        
        if final_score < 40:
            print("✅ 去痕成功！AI特征已大幅降低")
        else:
            print("⚠️ 还有改进空间，建议再人工润色")
        
        return rewritten


# ===== 测试 =====
if __name__ == "__main__":
    test_text = """
    林晨缓缓地站起身，宛如一只刚刚破茧而出的蝴蝶，心中不禁激动万分。
    仿佛天地都在为他欢呼，眼前的景象十分壮观，格外震撼人心。
    这一切似乎都像是一场梦境，渐渐地，林晨才相信这是真的。
    他微微一笑，心中暗想，自己的努力终究没有白费。
    极其艰难的旅程，非常辛苦的奋斗，终于换来了此刻的成功。
    宛如重生一般，他慢慢地向前走去，轻轻地踏上了前方的道路。
    """
    
    detector = AIDetectorAndRewriter()
    
    print("测试前:")
    print("-"*40)
    print(test_text)
    print("-"*40)
    
    result = detector.check_and_rewrite(test_text)
    
    print("\n测试后:")
    print("-"*40)
    print(result)
    print("-"*40)
