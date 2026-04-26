#!/usr/bin/env python3
"""
RecruitIQ CLI — Screen resumes directly from the command line.

Usage:
  python screen_cli.py --jd job_description.txt --resumes ./resumes/
  python screen_cli.py --jd job_description.txt --resumes cv1.pdf cv2.txt
"""

import argparse
import glob
import os
import sys

# Ensure backend is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "backend"))

from app import (
    extract_text,
    extract_skills,
    extract_experience_years,
    parse_resume,
)


def banner():
    print("\n" + "═" * 58)
    print("   🎯  RecruitIQ — AI Resume Screener CLI")
    print("═" * 58)


def print_result(r, idx):
    bar_len = 30
    pct = r["final_score"] / 100
    filled = int(pct * bar_len)
    bar = "█" * filled + "░" * (bar_len - filled)

    rec_icon = {"Strong Hire": "✅", "Consider": "🟡", "Not Recommended": "❌"}.get(
        r["recommendation"], "❓"
    )

    print(f"\n  {'─'*50}")
    print(f"  #{r['rank']}  {r['name']}  ({r['filename']})")
    print(f"       {r['email']}  |  {r['experience_years']} yrs experience")
    print(f"\n  Score: [{bar}] {r['final_score']:.1f}%  {rec_icon} {r['recommendation']}")
    print(f"\n  ├─ Skill Match    : {r['skill_match_score']:.1f}%")
    print(f"  ├─ Content Rel.   : {r['tfidf_score']:.1f}%")
    print(f"  └─ Education      : {r['education_score']}")

    if r["matched_skills"]:
        print(f"\n  ✓ Matched : {', '.join(r['matched_skills'][:8])}")
    if r["missing_skills"]:
        print(f"  ✗ Missing : {', '.join(r['missing_skills'][:6])}")


def main():
    parser = argparse.ArgumentParser(description="AI Resume Screener CLI")
    parser.add_argument("--jd", required=True, help="Path to job description file (.txt)")
    parser.add_argument(
        "--resumes", nargs="+", required=True, help="Resume files or directory"
    )
    parser.add_argument("--top", type=int, default=None, help="Show top N candidates only")
    args = parser.parse_args()

    banner()

    # Load JD
    if not os.path.exists(args.jd):
        print(f"\n[ERROR] JD file not found: {args.jd}")
        sys.exit(1)
    with open(args.jd, "r", encoding="utf-8") as f:
        jd_text = f.read()

    jd_skills = extract_skills(jd_text)
    jd_exp_req = extract_experience_years(jd_text)
    print(f"\n  JD Skills detected : {', '.join(jd_skills[:12]) or 'None'}")
    print(f"  Experience required: {jd_exp_req} years")

    # Collect resume paths
    resume_files = []
    for item in args.resumes:
        if os.path.isdir(item):
            resume_files.extend(glob.glob(os.path.join(item, "*.pdf")))
            resume_files.extend(glob.glob(os.path.join(item, "*.txt")))
        else:
            resume_files.append(item)

    if not resume_files:
        print("\n[ERROR] No resume files found.")
        sys.exit(1)

    print(f"\n  📂 Found {len(resume_files)} resume(s). Analyzing…\n")

    results = []
    for fp in resume_files:
        try:
            result = parse_resume(fp, jd_text, jd_skills, jd_exp_req)
            if result:
                results.append(result)
            else:
                print(f"  ⚠  Could not extract text from: {os.path.basename(fp)}")
        except Exception as e:
            print(f"  ⚠  Error processing {os.path.basename(fp)}: {e}")

    if not results:
        print("  No valid resumes could be processed.")
        sys.exit(1)

    # Rank
    results.sort(key=lambda x: x["final_score"], reverse=True)
    for i, r in enumerate(results):
        r["rank"] = i + 1
        r["recommendation"] = (
            "Strong Hire" if r["final_score"] >= 75
            else "Consider" if r["final_score"] >= 50
            else "Not Recommended"
        )

    top_n = args.top if args.top else len(results)
    print(f"\n{'═'*58}")
    print(f"  RANKED RESULTS  (showing top {min(top_n, len(results))} of {len(results)})")
    print(f"{'═'*58}")

    for r in results[:top_n]:
        print_result(r, r["rank"])

    # Summary
    hires    = sum(1 for r in results if r["recommendation"] == "Strong Hire")
    consider = sum(1 for r in results if r["recommendation"] == "Consider")
    no_hire  = sum(1 for r in results if r["recommendation"] == "Not Recommended")

    print(f"\n\n{'─'*58}")
    print(f"  SUMMARY: ✅ {hires} Strong Hire  |  🟡 {consider} Consider  |  ❌ {no_hire} Not Recommended")
    print(f"{'═'*58}\n")


if __name__ == "__main__":
    main()
