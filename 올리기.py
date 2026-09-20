#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
깃허브에 올리기

이 파일이 있는 폴더의 변경사항을 전부 깃허브에 올립니다.
더블클릭하면 됩니다.
"""

import os
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))


def run(*a):
    return subprocess.run(a, cwd=ROOT, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT)


def out(p):
    return p.stdout.decode("utf-8", "replace").strip()


def main():
    print("깃허브에 올리기")
    print("폴더:", ROOT)
    print()

    if not os.path.isdir(os.path.join(ROOT, ".git")):
        print("!! 이 폴더는 깃허브와 연결돼 있지 않습니다.")
        input("\n엔터를 누르면 닫힙니다...")
        return

    run("git", "config", "user.name", "wonbi")
    run("git", "config", "user.email", "wonbi@users.noreply.github.com")

    st = out(run("git", "status", "--porcelain"))
    if not st:
        print("바뀐 게 없습니다. 이미 최신입니다.")
        input("\n엔터를 누르면 닫힙니다...")
        return

    print("바뀐 파일")
    for line in st.splitlines()[:20]:
        print("  ", line)
    print()

    print("올리는 중 — 로그인 창이 뜨면 승인하세요")
    run("git", "add", "-A")
    run("git", "commit", "-m", "콘텐츠 업데이트")
    p = run("git", "push")
    if p.returncode != 0:
        run("git", "pull", "--rebase", "--autostash")
        p = run("git", "push")

    if p.returncode == 0:
        print("   OK 올라갔습니다")
        print("   https://github.com/wonbi/hansang-auto/actions")
    else:
        print("   !! 실패")
        print(out(p)[:800])
        print("   로그인 창이 뒤에 숨어 있는지 확인해 보세요 (Alt+Tab)")

    input("\n엔터를 누르면 닫힙니다...")


if __name__ == "__main__":
    main()
