"""命令行：compare / ask。"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .compare import DocComparator


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="multi-doc-compare",
                                 description="多文档对比问答（无 LLM 规则版）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    pc = sub.add_parser("compare", help="对多份文档做对齐/找差异与共识")
    pc.add_argument("files", nargs="+")
    pc.add_argument("--threshold", type=float, default=0.25)
    pc.add_argument("--json", action="store_true")
    pc.set_defaults(func=_cmd_compare)

    pa = sub.add_parser("ask", help="针对问题在各文档中找相关句子")
    pa.add_argument("question")
    pa.add_argument("files", nargs="+")
    pa.add_argument("--top", type=int, default=2)
    pa.set_defaults(func=_cmd_ask)

    args = ap.parse_args(argv)
    return args.func(args)


def _cmd_compare(args) -> int:
    for f in args.files:
        if not Path(f).exists():
            print(f"文件不存在: {f}", file=sys.stderr)
            return 2
    cmp = DocComparator(args.files)
    rep = cmp.compare(sim_threshold=args.threshold)
    if args.json:
        print(json.dumps(rep.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(rep.render())
    return 0


def _cmd_ask(args) -> int:
    for f in args.files:
        if not Path(f).exists():
            print(f"文件不存在: {f}", file=sys.stderr)
            return 2
    cmp = DocComparator(args.files)
    out = cmp.answer(args.question, top_per_doc=args.top)
    for doc, hits in out.items():
        print(f"## {doc}")
        if not hits:
            print("  （无相关句）")
        for score, text in hits:
            print(f"  [{score:.2f}] {text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
