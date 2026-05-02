#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
NWACS团队协作系统基础架构
支持多用户、角色权限、项目管理
"""

import os
import json
import uuid
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class TeamUser:
    """团队用户"""

    def __init__(self, user_id: str, username: str, role: str = "author"):
        self.user_id = user_id
        self.username = username
        self.role = role
        self.created_at = datetime.now().isoformat()
        self.last_active = datetime.now().isoformat()

    def to_dict(self) -> Dict:
        return {
            "user_id": self.user_id,
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at,
            "last_active": self.last_active
        }


class TeamProject:
    """团队项目"""

    def __init__(self, project_id: str, name: str, description: str = "", owner_id: str = None):
        self.project_id = project_id
        self.name = name
        self.description = description
        self.owner_id = owner_id
        self.members = []
        self.chapters = []
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()
        self.status = "active"

    def add_member(self, user_id: str, role: str = "editor"):
        """添加成员"""
        self.members.append({
            "user_id": user_id,
            "role": role,
            "joined_at": datetime.now().isoformat()
        })
        self.updated_at = datetime.now().isoformat()

    def remove_member(self, user_id: str):
        """移除成员"""
        self.members = [m for m in self.members if m["user_id"] != user_id]
        self.updated_at = datetime.now().isoformat()

    def add_chapter(self, chapter_data: Dict):
        """添加章节"""
        chapter = {
            "chapter_id": str(uuid.uuid4())[:8],
            "title": chapter_data.get("title", "未命名章节"),
            "content": chapter_data.get("content", ""),
            "author_id": chapter_data.get("author_id"),
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "comments": []
        }
        self.chapters.append(chapter)
        self.updated_at = datetime.now().isoformat()
        return chapter["chapter_id"]

    def to_dict(self) -> Dict:
        return {
            "project_id": self.project_id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "members": self.members,
            "chapters": self.chapters,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "status": self.status
        }


class TeamCollaborationSystem:
    """团队协作系统"""

    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path(__file__).parent.parent
        self.team_dir = self.project_root / "user_data" / "teams"
        self.team_dir.mkdir(parents=True, exist_ok=True)
        self.users_file = self.team_dir / "users.json"
        self.projects_file = self.team_dir / "projects.json"
        self._init_files()

    def _init_files(self):
        """初始化文件"""
        if not self.users_file.exists():
            self._save_users({})
        if not self.projects_file.exists():
            self._save_projects({})

    def _load_users(self) -> Dict:
        with open(self.users_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_users(self, users: Dict):
        with open(self.users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, ensure_ascii=False, indent=2)

    def _load_projects(self) -> Dict:
        with open(self.projects_file, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_projects(self, projects: Dict):
        with open(self.projects_file, 'w', encoding='utf-8') as f:
            json.dump(projects, f, ensure_ascii=False, indent=2)

    # ========================================
    # 用户管理
    # ========================================

    def create_user(self, username: str, role: str = "author") -> Dict:
        """创建用户"""
        user_id = str(uuid.uuid4())[:8]
        user = TeamUser(user_id, username, role)

        users = self._load_users()
        users[user_id] = user.to_dict()
        self._save_users(users)

        return {"success": True, "user": user.to_dict()}

    def get_user(self, user_id: str) -> Optional[Dict]:
        """获取用户"""
        users = self._load_users()
        return users.get(user_id)

    def list_users(self) -> List[Dict]:
        """列出所有用户"""
        users = self._load_users()
        return list(users.values())

    # ========================================
    # 项目管理
    # ========================================

    def create_project(self, name: str, description: str = "", owner_id: str = None) -> Dict:
        """创建项目"""
        project_id = str(uuid.uuid4())[:8]
        project = TeamProject(project_id, name, description, owner_id)

        projects = self._load_projects()
        projects[project_id] = project.to_dict()
        self._save_projects(projects)

        return {"success": True, "project": project.to_dict()}

    def get_project(self, project_id: str) -> Optional[Dict]:
        """获取项目"""
        projects = self._load_projects()
        return projects.get(project_id)

    def list_projects(self, user_id: str = None) -> List[Dict]:
        """列出项目"""
        projects = self._load_projects()
        if user_id:
            return [p for p in projects.values()
                   if p.get("owner_id") == user_id or
                   any(m["user_id"] == user_id for m in p.get("members", []))]
        return list(projects.values())

    def update_project(self, project_id: str, updates: Dict) -> Dict:
        """更新项目"""
        projects = self._load_projects()
        if project_id not in projects:
            return {"success": False, "error": "项目不存在"}

        projects[project_id].update(updates)
        projects[project_id]["updated_at"] = datetime.now().isoformat()
        self._save_projects(projects)

        return {"success": True, "project": projects[project_id]}

    def delete_project(self, project_id: str) -> Dict:
        """删除项目"""
        projects = self._load_projects()
        if project_id in projects:
            del projects[project_id]
            self._save_projects(projects)
            return {"success": True, "message": "项目已删除"}
        return {"success": False, "error": "项目不存在"}

    # ========================================
    # 章节管理
    # ========================================

    def add_chapter(self, project_id: str, chapter_data: Dict) -> Dict:
        """添加章节"""
        projects = self._load_projects()
        if project_id not in projects:
            return {"success": False, "error": "项目不存在"}

        project = projects[project_id]
        chapter_id = str(uuid.uuid4())[:8]
        chapter = {
            "chapter_id": chapter_id,
            "title": chapter_data.get("title", "未命名章节"),
            "content": chapter_data.get("content", ""),
            "author_id": chapter_data.get("author_id"),
            "status": "draft",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "comments": []
        }
        project["chapters"].append(chapter)
        project["updated_at"] = datetime.now().isoformat()
        self._save_projects(projects)

        return {"success": True, "chapter": chapter}

    def update_chapter(self, project_id: str, chapter_id: str, updates: Dict) -> Dict:
        """更新章节"""
        projects = self._load_projects()
        if project_id not in projects:
            return {"success": False, "error": "项目不存在"}

        project = projects[project_id]
        for chapter in project["chapters"]:
            if chapter["chapter_id"] == chapter_id:
                chapter.update(updates)
                chapter["updated_at"] = datetime.now().isoformat()
                project["updated_at"] = datetime.now().isoformat()
                self._save_projects(projects)
                return {"success": True, "chapter": chapter}

        return {"success": False, "error": "章节不存在"}

    def add_comment(self, project_id: str, chapter_id: str, comment: Dict) -> Dict:
        """添加评论"""
        projects = self._load_projects()
        if project_id not in projects:
            return {"success": False, "error": "项目不存在"}

        project = projects[project_id]
        for chapter in project["chapters"]:
            if chapter["chapter_id"] == chapter_id:
                comment_data = {
                    "comment_id": str(uuid.uuid4())[:8],
                    "user_id": comment.get("user_id"),
                    "username": comment.get("username", "匿名"),
                    "content": comment.get("content", ""),
                    "created_at": datetime.now().isoformat()
                }
                chapter["comments"].append(comment_data)
                self._save_projects(projects)
                return {"success": True, "comment": comment_data}

        return {"success": False, "error": "章节不存在"}


def interactive_demo():
    """交互式演示"""
    system = TeamCollaborationSystem()

    print("="*60)
    print("👥 NWACS团队协作系统 - 演示")
    print("="*60)

    # 创建用户
    print("\n📝 创建用户...")
    result = system.create_user("张三", "admin")
    user1 = result["user"]
    print(f"✅ 创建用户: {user1['username']} (ID: {user1['user_id']})")

    result = system.create_user("李四", "editor")
    user2 = result["user"]
    print(f"✅ 创建用户: {user2['username']} (ID: {user2['user_id']})")

    # 创建项目
    print("\n📚 创建项目...")
    result = system.create_project("我的小说", "一部玄幻小说", user1["user_id"])
    project = result["project"]
    print(f"✅ 创建项目: {project['name']} (ID: {project['project_id']})")

    # 添加成员
    print("\n👥 添加成员...")
    project_obj = TeamProject(project["project_id"], project["name"])
    project_obj.members = project["members"]
    project_obj.add_member(user2["user_id"], "editor")
    print(f"✅ 添加成员: {user2['username']}")

    # 添加章节
    print("\n📖 添加章节...")
    result = system.add_chapter(project["project_id"], {
        "title": "第一章 废物崛起",
        "content": "青云宗大殿，十年一度的资质测试正在进行...",
        "author_id": user1["user_id"]
    })
    chapter = result["chapter"]
    print(f"✅ 添加章节: {chapter['title']} (ID: {chapter['chapter_id']})")

    # 添加评论
    print("\n💬 添加评论...")
    result = system.add_comment(project["project_id"], chapter["chapter_id"], {
        "user_id": user2["user_id"],
        "username": user2["username"],
        "content": "开头不错，建议增加一些悬念"
    })
    print(f"✅ 添加评论: {result['comment']['content']}")

    # 显示项目信息
    print("\n" + "="*60)
    print("📊 项目信息")
    print("="*60)
    final_project = system.get_project(project["project_id"])
    print(f"项目名称: {final_project['name']}")
    print(f"章节数: {len(final_project['chapters'])}")
    print(f"成员数: {len(final_project['members'])}")
    print(f"评论数: {len(final_project['chapters'][0]['comments'])}")

    print("\n✅ 团队协作系统演示完成！")


if __name__ == "__main__":
    interactive_demo()
