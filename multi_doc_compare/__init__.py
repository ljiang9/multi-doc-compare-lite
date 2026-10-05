"""multi_doc_compare: 多文档对比问答。"""
from .compare import DocComparator, CompareReport
from .tokenize import tokenize, shingles

__all__ = ["DocComparator", "CompareReport", "tokenize", "shingles"]
__version__ = "0.1.0"
