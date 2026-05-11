#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS Web界面 - Streamlit原型

集成所有核心模块的统一Web操作界面：
- 创作工作台: 写作/续写/改写
- 设定管理: StoryBible + Lorebook
- 风格切换: StyleModuleManager
- 版本管理: VersionManager
- 角色命名: ChineseTraditionalNamer
- 剧情构思: PlotBrainstormEngine
- AI检测: EnhancedAIDetector
- 记忆验证: NovelMemoryManager

启动方式: streamlit run web_app.py
"""

import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from lorebook import Lorebook, LorebookEntry, EntryCategory, EntryPriority
from story_bible import StoryBible, BibleEntry, BibleSection
from style_module_manager import StyleModuleManager, StyleCategory
from version_manager import VersionManager, SnapshotType
from chinese_traditional_namer import ChineseTraditionalNamer
from plot_brainstorm_engine import PlotBrainstormEngine, PlotArcType
from enhanced_ai_detector import EnhancedAIDetector
from novel_memory_manager import NovelMemoryManager
from self_learning_engine import SelfLearningEngine

st.set_page_config(
    page_title="NWACS - 智能小说写作系统",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
    .main-header { font-size: 2rem; font-weight: bold; color: #1f77b4; margin-bottom: 1rem; }
    .section-header { font-size: 1.3rem; font-weight: bold; color: #333; margin-top: 1rem; }
    .stButton button { width: 100%; }
    .success-box { background-color: #d4edda; padding: 1rem; border-radius: 5px; }
    .warning-box { background-color: #fff3cd; padding: 1rem; border-radius: 5px; }
</style>
""", unsafe_allow_html=True)

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    st.session_state.lorebook = Lorebook()
    st.session_state.bible = StoryBible("我的小说")
    st.session_state.style_mgr = StyleModuleManager()
    st.session_state.version_mgr = VersionManager("我的小说")
    st.session_state.namer = ChineseTraditionalNamer()
    st.session_state.plotter = PlotBrainstormEngine()
    st.session_state.detector = EnhancedAIDetector()
    st.session_state.memory = NovelMemoryManager("我的小说")
    st.session_state.learner = SelfLearningEngine()
    st.session_state.current_text = ""
    st.session_state.current_chapter = 1

st.sidebar.markdown("## 📝 NWACS")
st.sidebar.markdown("智能小说写作系统 v8.1")

page = st.sidebar.radio(
    "导航",
    ["🏠 工作台", "📖 创作圣经", "🎨 风格管理", "📜 版本历史",
     "🔮 角色命名", "💡 剧情构思", "🔍 AI检测", "🧠 记忆验证",
     "📚 学习引擎", "📊 系统状态"],
)

if page == "🏠 工作台":
    st.markdown('<p class="main-header">📝 创作工作台</p>', unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        chapter = st.number_input("章节", min_value=1, value=st.session_state.current_chapter)
        st.session_state.current_chapter = chapter

        text = st.text_area(
            "写作区域",
            value=st.session_state.current_text,
            height=400,
            placeholder="在此开始创作...",
        )

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            if st.button("💾 保存", use_container_width=True):
                if text.strip():
                    st.session_state.version_mgr.create_snapshot(
                        chapter, text, SnapshotType.MANUAL, "手动保存"
                    )
                    st.session_state.memory.record_chapter(chapter, text)
                    st.session_state.current_text = text
                    st.success(f"第{chapter}章已保存！")
        with c2:
            if st.button("🤖 AI续写", use_container_width=True):
                st.info("AI续写功能需要配置DeepSeek API")
        with c3:
            if st.button("✨ 润色", use_container_width=True):
                st.info("润色功能需要配置DeepSeek API")
        with c4:
            if st.button("🔍 检测", use_container_width=True):
                if text.strip():
                    result = st.session_state.detector.detect(text)
                    st.metric("AI痕迹分数", f"{result.final_score:.0f}/100")

    with col2:
        st.markdown("### 📋 快捷操作")
        active_style = st.session_state.style_mgr.active_module
        if active_style:
            st.info(f"当前风格: **{active_style.name}**")

        lore_stats = st.session_state.lorebook.get_stats()
        st.metric("设定条目", lore_stats["total_entries"])
        st.metric("触发关键词", lore_stats["keyword_count"])

        ver_stats = st.session_state.version_mgr.get_stats()
        st.metric("版本快照", ver_stats["total_snapshots"])

        if text.strip():
            triggered = st.session_state.lorebook.trigger(text, chapter)
            if triggered:
                st.markdown("### 🔔 触发设定")
                for entry in triggered[:5]:
                    with st.expander(f"{entry.category.value}: {entry.name}"):
                        st.write(entry.content)

elif page == "📖 创作圣经":
    st.markdown('<p class="main-header">📖 创作圣经 (Story Bible)</p>', unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["灵感碎片", "角色档案", "世界观"])

    with tab1:
        st.text_area("故事梗概", height=150, key="synopsis",
                      placeholder="用一段话概括你的故事...")
        st.text_area("灵感碎片", height=200, key="braindump",
                      placeholder="记录所有灵感、想法、片段...")

    with tab2:
        col_a, col_b = st.columns([3, 1])
        with col_a:
            char_name = st.text_input("角色名称", key="char_name")
            char_desc = st.text_area("角色描述", height=150, key="char_desc")
        with col_b:
            char_role = st.selectbox("角色定位", ["主角", "配角", "反派", "导师", "盟友", "路人"])
            char_gender = st.selectbox("性别", ["男", "女", "其他"])
        if st.button("添加角色"):
            if char_name:
                entry = BibleEntry(
                    entry_id="", section=BibleSection.CHARACTERS,
                    title=char_name, content=char_desc,
                    tags=[char_role, char_gender],
                    metadata={"name": char_name, "role": char_role, "gender": char_gender},
                )
                st.session_state.bible.add_entry(entry)
                st.success(f"角色 {char_name} 已添加！")

        characters = st.session_state.bible.get_section(BibleSection.CHARACTERS)
        if characters:
            for char in characters:
                with st.expander(f"{char.title} ({', '.join(char.tags)})"):
                    st.write(char.content)

    with tab3:
        world_name = st.text_input("世界名称", key="world_name")
        world_desc = st.text_area("世界观描述", height=200, key="world_desc",
                                   placeholder="描述你的世界设定...")
        if st.button("保存世界观"):
            if world_name:
                entry = BibleEntry(
                    entry_id="", section=BibleSection.WORLD_BUILDING,
                    title=world_name, content=world_desc,
                    tags=["世界观"],
                )
                st.session_state.bible.add_entry(entry)
                st.success("世界观已保存！")

elif page == "🎨 风格管理":
    st.markdown('<p class="main-header">🎨 风格模块管理</p>', unsafe_allow_html=True)

    modules = st.session_state.style_mgr.list_modules()
    active = st.session_state.style_mgr.active_module

    cols = st.columns(3)
    for i, module in enumerate(modules):
        with cols[i % 3]:
            is_active = active and active.module_id == module.module_id
            border = "2px solid #1f77b4" if is_active else "1px solid #ddd"
            st.markdown(f"""
            <div style="border:{border}; border-radius:10px; padding:15px; margin-bottom:10px;">
                <h4>{'⭐ ' if is_active else ''}{module.name}</h4>
                <p style="color:#666; font-size:0.9rem;">{module.description}</p>
                <p style="font-size:0.8rem;">标签: {', '.join(module.tags) if module.tags else '无'}</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("激活" if not is_active else "已激活 ✓", key=f"act_{module.module_id}"):
                st.session_state.style_mgr.activate(module.module_id)
                st.rerun()

elif page == "📜 版本历史":
    st.markdown('<p class="main-header">📜 版本历史</p>', unsafe_allow_html=True)

    stats = st.session_state.version_mgr.get_stats()
    c1, c2, c3 = st.columns(3)
    c1.metric("总快照", stats["total_snapshots"])
    c2.metric("分支数", stats["total_branches"])
    c3.metric("当前分支", stats["current_branch"])

    log = st.session_state.version_mgr.get_change_log(30)
    if log:
        st.markdown("### 变更记录")
        for entry in log:
            st.markdown(
                f"- `{entry['snapshot_id']}` | 第{entry['chapter']}章 | "
                f"{entry['type']} | {entry['word_count']}字 | {entry['timestamp'][:19]}"
            )

elif page == "🔮 角色命名":
    st.markdown('<p class="main-header">🔮 角色命名</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        gender = st.selectbox("性别", ["男", "女"])
        surname = st.text_input("姓氏（留空则随机）", placeholder="如：叶、苏、林...")
    with col2:
        style = st.selectbox("风格", ["仙侠古风", "现代都市", "武侠江湖", "诗意文艺"])
        count = st.slider("生成数量", 1, 10, 5)

    if st.button("🎲 生成名字", use_container_width=True):
        names = st.session_state.namer.generate_names(
            gender=gender, surname=surname if surname else None,
            count=count, style=style,
        )
        st.markdown("### 生成结果")
        for name in names:
            st.markdown(f"""
            <div style="border:1px solid #ddd; border-radius:8px; padding:12px; margin:8px 0;">
                <span style="font-size:1.3rem; font-weight:bold;">{name['full_name']}</span>
                <span style="color:#888; margin-left:10px;">{name.get('meaning', '')}</span>
                <br><small>五行: {name.get('wuxing', '')} | 笔画: {name.get('strokes', '')}</small>
            </div>
            """, unsafe_allow_html=True)

elif page == "💡 剧情构思":
    st.markdown('<p class="main-header">💡 剧情构思</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        arc_type = st.selectbox("剧情弧线", [a.value for a in PlotArcType])
        total_chapters = st.number_input("总章节数", 10, 500, 60)
    with col2:
        genre = st.selectbox("题材", ["玄幻", "仙侠", "都市", "言情", "悬疑", "科幻", "历史", "游戏"])
        theme = st.text_input("核心主题", placeholder="如：复仇、成长、救赎...")

    if st.button("🎭 生成剧情弧线", use_container_width=True):
        arc = st.session_state.plotter.design_plot_arc(
            PlotArcType(arc_type), total_chapters, genre
        )
        st.markdown(f"### {arc_type} 结构")
        for i, node in enumerate(arc.nodes):
            st.markdown(f"""
            <div style="border-left:3px solid #1f77b4; padding:8px 15px; margin:5px 0;">
                <strong>节点{i+1}:</strong> 第{node.get('chapter', '?')}章 - {node.get('description', '')}
            </div>
            """, unsafe_allow_html=True)

elif page == "🔍 AI检测":
    st.markdown('<p class="main-header">🔍 AI内容检测</p>', unsafe_allow_html=True)

    test_text = st.text_area(
        "输入待检测文本",
        height=200,
        placeholder="粘贴需要检测的文本...",
    )

    if st.button("🔍 开始检测", use_container_width=True):
        if test_text.strip():
            result = st.session_state.detector.detect(test_text)
            col1, col2, col3 = st.columns(3)
            col1.metric("AI痕迹分数", f"{result.final_score:.0f}/100",
                       delta="低风险" if result.final_score < 30 else (
                           "中风险" if result.final_score < 60 else "高风险"))
            col2.metric("原始分数", f"{result.original_score:.0f}/100")
            col3.metric("检测层数", "3层")

            if result.final_score > 50:
                st.warning("⚠️ 该文本AI痕迹较重，建议进行去痕处理")
                if st.button("🔄 AI去痕"):
                    rewritten, new_result = st.session_state.detector.rewrite(test_text, "medium")
                    st.text_area("去痕后文本", rewritten, height=200)
                    st.metric("去痕后分数", f"{new_result.final_score:.0f}/100")
            else:
                st.success("✅ 该文本AI痕迹较轻")

elif page == "🧠 记忆验证":
    st.markdown('<p class="main-header">🧠 记忆一致性验证</p>', unsafe_allow_html=True)

    stats = st.session_state.memory.get_stats()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("已记录章节", stats.get("total_chapters", 0))
    c2.metric("角色数", stats.get("character_count", 0))
    c3.metric("伏笔数", stats.get("foreshadowing_count", 0))
    c4.metric("一致性问题", stats.get("issue_count", 0))

    if stats.get("foreshadowing_count", 0) > 0:
        st.markdown("### 伏笔状态")
        foreshadowings = st.session_state.memory.get_foreshadowings()
        for fs in foreshadowings:
            status_color = "green" if fs.status.value == "已回收" else "orange"
            st.markdown(
                f"- 🏷️ 第{fs.chapter}章: {fs.description} "
                f"<span style='color:{status_color}'>[{fs.status.value}]</span>",
                unsafe_allow_html=True,
            )

elif page == "📚 学习引擎":
    st.markdown('<p class="main-header">📚 自学习引擎</p>', unsafe_allow_html=True)

    report = st.session_state.learner.get_skill_report()
    st.markdown("### 技能状态")

    for key, info in report.items():
        level_color = {
            "新手": "#999", "学徒": "#666", "熟手": "#1f77b4",
            "专家": "#28a745", "大师": "#ffc107", "宗师": "#dc3545",
        }.get(info["level"], "#999")

        st.markdown(f"""
        <div style="display:flex; align-items:center; margin:8px 0;">
            <span style="width:100px; font-weight:bold;">{info['display']}</span>
            <span style="color:{level_color}; font-weight:bold; width:60px;">{info['level']}</span>
            <div style="flex:1; background:#eee; height:20px; border-radius:10px; margin:0 10px;">
                <div style="width:{info['experience'] / info['max_experience'] * 100}%;
                     background:{level_color}; height:100%; border-radius:10px;"></div>
            </div>
            <span style="font-size:0.8rem;">{info['experience']}/{info['max_experience']}</span>
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 系统状态":
    st.markdown('<p class="main-header">📊 系统状态</p>', unsafe_allow_html=True)

    st.markdown("### 模块状态总览")

    modules_status = [
        ("Lorebook 触发式设定", "✅", st.session_state.lorebook.get_stats()),
        ("Story Bible 创作圣经", "✅", st.session_state.bible.get_stats()),
        ("Style Manager 风格管理", "✅", st.session_state.style_mgr.get_stats()),
        ("Version Manager 版本管理", "✅", st.session_state.version_mgr.get_stats()),
        ("Chinese Namer 命名系统", "✅", {"surnames": len(st.session_state.namer.surnames)}),
        ("Plot Engine 剧情引擎", "✅", {}),
        ("AI Detector 检测器", "✅", {}),
        ("Memory Manager 记忆", "✅", st.session_state.memory.get_stats()),
        ("Learning Engine 学习", "✅", {"skills": len(st.session_state.learner.get_skill_report())}),
    ]

    for name, status, stats in modules_status:
        with st.expander(f"{status} {name}"):
            st.json(stats)

st.sidebar.markdown("---")
st.sidebar.markdown("NWACS v8.1 | © 2026")
st.sidebar.markdown("[GitHub](https://github.com/dddyang1477/nwacs)")
