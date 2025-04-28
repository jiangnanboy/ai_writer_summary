import os
import json
from datetime import datetime
from textwrap import dedent
from typing import Optional, Dict, Any, List, Tuple
from pydantic_ai.models.openai import OpenAIModel

from .agents import PlannerAgent, SummaryAgent
from .types import ArticlePlan, ArticleSection


class ArticleSummary:
    
    def __init__(
        self, 
        model: OpenAIModel = None,
    ):
        """
        Args:
            model (OpenAIModel): 用于生成的AI模型。
        """
        self.model = model
        self.planner = PlannerAgent(model)
        self.writer = SummaryAgent(model)
    
    def generate(
        self, 
        topic: str, 
    ) -> Tuple[str, Dict[str, Any]]:
        """
        根据给定的主题和字数生成一篇文章。

        Args:
            topic (str): 文章主题。

        Returns:
            Tuple[str, Dict[str, Any]]: markdown内容和文章数据。
        """

        # Planning
        print("文章总结规划中...")
        plan = self.planner.plan(topic)
        print("文章总结规划创建成功！\n")
        
        # Generate content
        print("内容总结中...")
        sections = self._generate_sections(plan)
        print("所有章节创建成功！\n")
        
        # Combine sections
        print("将章节组合成一篇完整的...")
        markdown_content = self._combine_sections(plan, sections)
        print("文章观点创建成功！\n")
        
        # Prepare article data
        plan_dict = plan.model_dump()
        sections_dict = [section.model_dump() for section in sections]
        
        article_data = {
            "plan": plan_dict,
            "sections": sections_dict,
        }

        
        return markdown_content, article_data
    
    def _generate_sections(self, plan: ArticlePlan) -> List[ArticleSection]:
        """
        生成文章的所有总结观点。

        Args:
            plan (ArticlePlan): 文章总结规划.
            
        Returns:
            List[ArticleSection]: 生成的章节列表。
        """
        sections = []
        
        # Create body sections
        section_count = len(plan.outline.sections)
        for section_index in range(section_count):
            print(f"章节 {section_index + 1}/{section_count}: {plan.outline.sections[section_index].title}")
            section = self.writer.write_section(plan, section_index)
            sections.append(section)
        
        # Create conclusion
        print("创建结论中...")
        conclusion = self.writer.write_conclusion(plan)
        sections.append(conclusion)
        
        return sections
    
    def _combine_sections(self, plan: ArticlePlan, sections: List[ArticleSection]) -> str:
        """
        将所有章节组合成一个完整的markdown文档。

        Args:
            plan (ArticlePlan): 文章规划。
            sections (List[ArticleSection]): 章节列表。
            
        Returns:
            str: The complete markdown content.
        """
        # Create title section
        title_section = f"# {plan.outline.title}\n\n"
        if plan.outline.subtitle:
            title_section += f"*{plan.outline.subtitle}*\n\n"
        
        # Combine all markdown sections
        return title_section + "\n\n".join([section.markdown_content for section in sections])

def summary_article(
    topic: str, 
    model: OpenAIModel = None,
) -> str:
    """
    生成文章
    Args:
        topic (str): 文章主题。
        model (OpenAIModel): AI模型。

    Returns:
        str: The markdown content.
    """
    generator = ArticleSummary(model=model)
    markdown_content, _ = generator.generate(topic)
    return markdown_content
