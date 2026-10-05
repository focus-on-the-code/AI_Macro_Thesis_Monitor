"""Validate Phase 0 cost controls and cross-document definition freeze."""
import hashlib
import json
from pathlib import Path
import re

import jsonschema
import yaml

ROOT = Path(__file__).resolve().parents[1]


def validate():
    spec = yaml.safe_load((ROOT / 'AI_Macro_Thesis_Monitor_Agent_Build_Spec_v0.91.yaml').read_text())
    prd = (ROOT / 'AI_Macro_Thesis_Monitor_PRD_v0.91.md').read_text()
    schema = json.loads((ROOT / 'schemas/build-spec.schema.json').read_text())
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(spec, schema)
    for path, digest in json.loads((ROOT / 'registry/source-baseline.json').read_text()).items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert [p['id'] for p in spec['panels']] == [f'V{i}' for i in range(1, 8)]
    pages_section = prd.split('## 6. Approved information architecture')[1].split('## 7.')[0]
    assert re.findall(r'^- \*\*(.*?):\*\*', pages_section, re.M) == spec['pages']
    inventory = json.loads((ROOT / 'registry/formula-inventory.json').read_text())
    expected = []
    for panel in spec['panels']:
        section = prd.split(f"### {panel['id']} - {panel['name']}\n", 1)[1]
        section = re.split(r'\n(?:### V\d|## 9\.)', section)[0]
        assert f"**Core question:** {panel['question']}" in section
        rows = re.findall(r'^\| (.*?) \| (.*?) \|$', section, re.M)[2:]
        assert rows == [(m['name'], m['definition']) for m in panel['metrics']]
        tickers = re.search(r'\*\*Relevant market tickers/instruments:\*\* (.*)', section)[1]
        assert tickers.split(', ') == panel['tickers']
        for index, metric in enumerate(panel['metrics'], 1):
            expected.append((f"{panel['id']}-F{index:02d}", panel['id'], metric['name'], metric['definition']))
    actual = [(x['formula_id'], x['panel_id'], x['metric'], x['definition']) for x in inventory]
    assert actual == expected
    assert all(x['definition_status'] == 'FROZEN_V0.91' and x['implementation_status'] == 'TBD'
               and x['unresolved'].startswith('TBD:') for x in inventory)
    print(f'P0-T04 PASS: schema, original hashes, 7 panels, 4 pages, {len(inventory)} metric definitions/formula IDs and ticker mappings')
    config = json.loads((ROOT / 'config/services.json').read_text())
    assert config['phase'] == 0
    assert config['hosted_actions_enabled'] is False and config['zero_overage_verified'] is False
    ids = {x['id'] for x in config['services']}
    assert {'market_data', 'premium_news', 'llm_api', 'hosting', 'object_storage',
            'actions_overages', 'paid_runners'} <= ids
    assert len(ids) == len(config['services'])
    assert all(x['enabled'] is False and x['provider'] == 'TBD'
               and x['approval'] == 'APPROVAL REQUIRED' and x['owner_approval_ref'] is None
               for x in config['services'])
    workflow = yaml.load((ROOT / '.github/workflows/phase0.yml').read_text(), Loader=yaml.BaseLoader)
    assert set(workflow['on']) == {'pull_request'}
    assert workflow['permissions'] == {'contents': 'read'}
    assert all(job['if'] == '${{ false }}' for job in workflow['jobs'].values())
    assert all(re.fullmatch(r'[A-Z_]+=', line)
               for line in (ROOT / '.env.example').read_text().splitlines())
    print('P0-T03 PASS: all 16 providers disabled/TBD; hosted job literal-false; empty secrets template')


if __name__ == '__main__':
    validate()
