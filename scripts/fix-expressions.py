"""Fix AI-like and exam-frequency expressions across all wiki pages.

공공조달관리사는 신규 1회 시험이므로 '빈출', '매년 출제', '자주 출제' 등 표현을 제거.
AI 티가 나는 과장된 표현도 자연스럽게 교정.
"""
import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# (pattern, replacement) — applied in order
REPLACEMENTS = [
    # 시험 빈도 관련 (1회 시험이므로 잘못된 표현)
    (r'시험에\s*매우\s*자주\s*출제된다', '시험에서 중요하게 다뤄진다'),
    (r'시험에\s*자주\s*출제된다', '시험에서 다뤄질 수 있다'),
    (r'매우\s*자주\s*출제', '핵심'),
    (r'시험에\s*자주\s*출제되는', '시험에서 중요한'),
    (r'자주\s*출제되는', '중요한'),
    (r'자주\s*출제', '중요'),
    (r'빈출\s*지문', '핵심 지문'),
    (r'빈출\s*포인트', '핵심 포인트'),
    (r'빈출', '핵심'),
    (r'매년\s*출제', '교재 핵심'),
    (r'단골\s*출제', '핵심'),
    (r'출제\s*빈도', '중요도'),
    (r'출제\s*가능성이\s*높은', '중요한'),
    (r'시험에\s*나올\s*가능성이\s*높', '알아둘 필요가 있'),

    # AI 티 나는 과장 표현
    (r'매우\s*중요한', '중요한'),
    (r'매우\s*중요하다', '중요하다'),
    (r'반드시\s*숙지해야', '이해해야'),
    (r'반드시\s*숙지할', '이해할'),
    (r'꼭\s*알아두어야', '알아두어야'),
    (r'꼭\s*기억해두자', '기억하자'),
    (r'반드시\s*기억해야', '기억해야'),
    (r'필수적으로\s*', '반드시 '),
    (r'절대적으로\s*', ''),
    (r'중요한\s*포인트로서?,\s*', ''),
    (r'핵심적인\s*내용이며,?\s*', ''),
]

def fix_content(content: str) -> tuple[str, int]:
    changes = 0
    for pat, rep in REPLACEMENTS:
        new_content, n = re.subn(pat, rep, content)
        if n > 0:
            changes += n
            content = new_content
    return content, changes

total_files = 0
total_changes = 0

for root, dirs, files in os.walk('wiki'):
    for f in files:
        if not f.endswith('.md'):
            continue
        fp = os.path.join(root, f)
        try:
            content = open(fp, encoding='utf-8').read()
        except Exception:
            continue
        new_content, changes = fix_content(content)
        if changes > 0:
            open(fp, 'w', encoding='utf-8').write(new_content)
            total_files += 1
            total_changes += changes

print(f'Modified files: {total_files}')
print(f'Total replacements: {total_changes}')
