# multi-doc-compare-lite

零依赖的多文档对比问答 CLI。对多份 `.txt` / `.md` 文档做句子级对齐，自动找出共识、潜在矛盾（肯否相反 / 数字冲突）和差异点，并支持跨文档问答。全程规则驱动，无需 LLM、无需 API Key。

## 快速开始

```bash
python -m multi_doc_compare compare a.txt b.txt c.txt
python -m multi_doc_compare ask "GIL 是什么" a.txt b.txt
```

## 无 API Key 如何运行

本工具默认就是规则版，不调用任何 LLM，不需要任何 Key。

## 运行测试

```bash
python -m unittest discover -s tests -v
```

## License

MIT © ljiang9
