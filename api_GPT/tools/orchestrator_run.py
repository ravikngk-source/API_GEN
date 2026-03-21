#!/usr/bin/env python3
import os
import json
import glob
import argparse
from pathlib import Path

def load_json(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return None

def check_extracted_schema(base):
    p = base / 'generated_schema' / 'extracted_schema.json'
    data = load_json(p)
    if not data or 'fields' not in data:
        return False, f'missing or invalid {p}'
    return True, str(p)

def try_copy_any(src_pattern, dst_path):
    # Find any matching file in workspace and copy to dst_path
    import shutil
    candidates = glob.glob(str(Path(__file__).resolve().parents[1] / '**' / src_pattern), recursive=True)
    for c in candidates:
        try:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(c, str(dst_path))
            return True, str(dst_path)
        except Exception:
            continue
    return False, None

def find_files(pattern):
    return sorted([str(Path(p)) for p in glob.glob(pattern)])

def check_positive(base, need):
    dirp = base / 'generated_schema' / 'Valid_positive'
    pattern = str(dirp / 'TC_POS_*.json')
    files = find_files(pattern)
    if len(files) < need:
        return False, files
    return True, files[:need]

def check_negative(base, need):
    dirp = base / 'generated_schema' / 'Valid_Negative'
    pattern = str(dirp / 'TC_NEG_*.json')
    files = find_files(pattern)
    if len(files) < need:
        return False, files
    return True, files[:need]

def check_validated(base):
    p = base / 'Payloads' / 'validated_payloads.json'
    data = load_json(p)
    if not data or not any(k in data for k in ('positive','negative','edge')):
        return False, f'missing or invalid {p}'
    return True, str(p)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pos', type=int, default=3, help='POS_COUNT')
    parser.add_argument('--neg', type=int, default=4, help='NEG_COUNT')
    parser.add_argument('--auto-populate', action='store_true', help='Try to auto-populate missing files from workspace copies')
    args = parser.parse_args()

    base = Path(__file__).resolve().parents[1]
    summary = {
        'extracted_schema': None,
        'positive_files': [],
        'negative_files': [],
        'validated_files': []
    }

    ok, res = check_extracted_schema(base)
    if not ok:
        if args.auto_populate:
            dst = base / 'generated_schema' / 'extracted_schema.json'
            found, path = try_copy_any('extracted_schema.json', dst)
            if found:
                ok, res = check_extracted_schema(base)
        if not ok:
            print(json.dumps({'error': res}))
            return 1
    summary['extracted_schema'] = res

    ok, files = check_positive(base, args.pos)
    if not ok and args.auto_populate:
        # try to find any TC_POS_*.json elsewhere and copy
        dirp = base / 'generated_schema' / 'Valid_positive'
        dirp.mkdir(parents=True, exist_ok=True)
        candidates = glob.glob(str(Path(__file__).resolve().parents[1] / '**' / 'TC_POS_*.json'), recursive=True)
        copied = []
        import shutil
        for c in sorted(candidates):
            dst = dirp / Path(c).name
            if not dst.exists():
                try:
                    shutil.copyfile(c, str(dst))
                    copied.append(str(dst))
                except Exception:
                    continue
        ok, files = check_positive(base, args.pos)
    if not ok:
        print(json.dumps({'error': f'positive files missing, found {len(files)} required {args.pos}'}))
        return 2
    summary['positive_files'] = files

    ok, files = check_negative(base, args.neg)
    if not ok and args.auto_populate:
        dirp = base / 'generated_schema' / 'Valid_Negative'
        dirp.mkdir(parents=True, exist_ok=True)
        candidates = glob.glob(str(Path(__file__).resolve().parents[1] / '**' / 'TC_NEG_*.json'), recursive=True)
        import shutil
        for c in sorted(candidates):
            dst = dirp / Path(c).name
            if not dst.exists():
                try:
                    shutil.copyfile(c, str(dst))
                except Exception:
                    continue
        ok, files = check_negative(base, args.neg)
    if not ok:
        print(json.dumps({'error': f'negative files missing, found {len(files)} required {args.neg}'}))
        return 3
    summary['negative_files'] = files

    ok, res = check_validated(base)
    if not ok and args.auto_populate:
        dst = base / 'Payloads' / 'validated_payloads.json'
        found, path = try_copy_any('validated_payloads.json', dst)
        if found:
            ok, res = check_validated(base)
    if not ok:
        print(json.dumps({'error': res}))
        return 4
    summary['validated_files'] = [res]

    out_path = base / 'prompt' / 'chain_summary.json'
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
