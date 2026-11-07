import math
import os
import re
from collections import Counter

NATURE = {
    'data_flow': 'data flow',
    'control_command': 'control command',
    'dependency': 'dependency',
    'event_notification': 'event notification',
}


def _kind(obj):
    return obj.__class__.__name__


def _components(model):
    return [e for e in model.elements if _kind(e) == 'Component']


def _connectors(model):
    return [e for e in model.elements if _kind(e) == 'Connector']


def _crosses(link):
    return len({c.system.name for c in link.path}) > 1


def _boundary(connector):
    crossing = [link for link in connector.links if _crosses(link)]
    if not crossing:
        return 'No'
    if len(crossing) == len(connector.links):
        return 'Yes'
    return 'Yes (' + ', '.join(link.path[0].label for link in crossing) + ')'


def _is_boundary(connector):
    return any(_crosses(link) for link in connector.links)


def _nid(name):
    """Mermaid node identifier: Delivery identifiers contain '.' and '-'."""
    return re.sub(r'\W', '_', name)


def _write(out, name, lines):
    with open(os.path.join(out, name), 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')


# ---------------------------------------------------
# Model-to-text: documentation
# ---------------------------------------------------

def generate_connector_table(model, out):
    lines = [f'# Connectors of {model.name}', '',
             '| ID | Source → Target | Nature | Coupling | Information '
             'carried | Boundary |',
             '|----|-----------------|--------|----------|----------------'
             '-----|----------|']
    for k in _connectors(model):
        paths = '; '.join(' → '.join(c.label for c in link.path)
                          for link in k.links)
        natures = ', '.join(NATURE[n] for n in k.natures).capitalize()
        lines.append(f'| {k.name} | {paths} | {natures} | '
                     f'{k.coupling.capitalize()} '
                     f'| {k.info} | {_boundary(k)} |')
    _write(out, 'connectors.md', lines)


# ---------------------------------------------------
# Model-to-text: graphical representation
# ---------------------------------------------------

def generate_view(model, out):
    lines = ['flowchart LR']
    for s in model.constituents:
        lines.append(f'  subgraph {s.name}["{s.label}"]')
        for c in _components(model):
            if c.system is s:
                nid = _nid(c.name)
                shape = (f'[("{c.label} ({c.tier})")]' if c.tier == 'T4'
                         else f'["{c.label} ({c.tier})"]')
                lines.append(f'    {nid}{shape}')
        lines.append('  end')
    for k in _connectors(model):
        for link in k.links:
            for a, b in zip(link.path, link.path[1:]):
                lines.append(f'  {_nid(a.name)} -->|{k.name}| {_nid(b.name)}')
    _write(out, 'view.mmd', lines)


# ---------------------------------------------------
# Model-to-text: structural summary (reproduces counts of Deliveries 1 and 2)
# ---------------------------------------------------

def generate_summary(model, out):
    comps = _components(model)
    conns = _connectors(model)
    lines = [f'# Summary of {model.name}', '',
             f'- Constituents: {len(model.constituents)}',
             f'- Components: {len(comps)}',
             f'- Connectors: {len(conns)}', '']

    lines += ['## Components by constituent and tier', '',
              '| Constituent | T1 | T2 | T3 | T4 | T5 | Total |',
              '|-------------|----|----|----|----|----|-------|']
    for s in model.constituents:
        mine = [c for c in comps if c.system is s]
        row = [sum(1 for c in mine if c.tier == t)
               for t in ('T1', 'T2', 'T3', 'T4', 'T5')]
        lines.append(f'| {s.name} | ' + ' | '.join(map(str, row)) +
                     f' | {len(mine)} |')

    boundary = [k for k in conns if _is_boundary(k)]
    internal = [k for k in conns if not _is_boundary(k)]
    lines += ['', '## Connectors by coupling', '',
              '| Class | Blocking | Supply | Sink | Total |',
              '|-------|----------|--------|------|-------|']
    for title, group in (('Internal', internal), ('Boundary (derived)',
                                                  boundary)):
        c = Counter(k.coupling for k in group)
        lines.append(f'| {title} | {c["blocking"]} | {c["supply"]} | '
                     f'{c["sink"]} | {len(group)} |')

    lines += ['', '## Connectors by nature', '',
              '| Nature | Internal | Boundary |', '|--------|----------|----------|']
    for n in NATURE:
        lines.append(f'| {NATURE[n]} | '
                     f'{sum(1 for k in internal if n in k.natures)} | '
                     f'{sum(1 for k in boundary if n in k.natures)} |')

    degree = Counter()
    for k in conns:
        for link in k.links:
            for c in link.path:
                degree[c.name] += 1
    lines += ['', '## Connectors per component (top 8)', '',
              '| Component | Connectors |', '|-----------|------------|']
    labels = {c.name: c.label for c in comps}
    for name, d in degree.most_common(8):
        lines.append(f'| {labels[name]} | {d} |')

    lines += ['', '## Boundary connectors (derived)', '',
              ', '.join(k.name for k in boundary)]
    _write(out, 'summary.md', lines)


# ---------------------------------------------------
# Transformation to analysis: scenarios
# ---------------------------------------------------

def _unavailability(factor):
    """Unavailability of a factor. A group of alternatives or a replicated
    element uses the common-cause fraction beta: beta*U + ((1 - beta)*U)^n."""
    kind = _kind(factor)
    if kind == 'Group':
        u = 1 - factor.alternatives[0].availability / 100
        b = factor.beta
        n = len(factor.alternatives)
        name = ', '.join(r.name for r in factor.alternatives)
        return b * u + ((1 - b) * u) ** n, f'{name} (β = {b:g})'
    if kind == 'Replicated':
        u = 1 - factor.ref.availability / 100
        b = factor.beta
        n = factor.count
        return (b * u + ((1 - b) * u) ** n,
                f'{factor.ref.name} × {n} (β = {b:g})')
    availability = factor.value or factor.ref.availability
    return 1 - availability / 100, factor.ref.name


def _analyze_utilization(analysis):
    rows, worst = [], 0.0
    for f in analysis.factors:
        r = f.ref
        instances = max(1, getattr(r, 'instances', 0) or 1)
        u = r.load / (r.capacity * instances) * 100
        needed = math.ceil(r.load / r.capacity)
        worst = max(worst, u)
        rows.append(f'| {r.name} | {r.load:g} | {r.capacity:g} | '
                    f'{instances} | {u:.0f} % | {needed} |')
    header = ['| Element | Load | Capacity per instance | Instances | '
              'Utilization | Instances needed |',
              '|---------|------|-----------------------|-----------|'
              '-------------|------------------|']
    summary = f'Bottleneck utilization: **{worst:.0f} %**'
    met = round(worst, 6) <= analysis.target
    return header, rows, summary, met


def analyze(analysis):
    rows = []
    if analysis.metric == 'availability':
        terms = [_unavailability(f) for f in analysis.factors]
        total_u = sum(u for u, _ in terms)
        result = 1.0
        for u, _ in terms:
            result *= 1 - u
        result *= 100
        for u, name in terms:
            rows.append(f'| {name} | {u * 100:.4f} % | '
                        f'{u / total_u * 100:.0f} % |')
        header = ['| Factor | Unavailability | Share |',
                  '|--------|----------------|-------|']
        hours = (100 - result) / 100 * 8760
        summary = f'Chain availability: **{result:.4f} %** ({hours:.1f} h/year)'
        met = round(result, 6) >= analysis.target
    elif analysis.metric == 'latency':
        result = 0.0
        for f in analysis.factors:
            budget = f.value or f.ref.latency
            result += budget
            rows.append(f'| {f.ref.name} | {budget:g} |')
        header = ['| Stage | Budget |', '|-------|--------|']
        summary = f'Chain latency: **{result:g}**'
        met = round(result, 6) <= analysis.target
    elif analysis.metric == 'deadline':
        # [D] Sum of the budgets of the stages; a group works in parallel and counts its maximum.
        result = 0
        for f in analysis.factors:
            if f.__class__.__name__ == 'Group':
                stage = max(m.value for m in f.members)
                names = ' ‖ '.join(f'{m.ref.name} ({m.value:g} s)' for m in f.members)
                rows.append(f'| {names} | {stage:g} s (maximum, in parallel) |')
            else:
                stage = f.value
                rows.append(f'| {f.ref.name} | {stage:g} s |')
            result += stage
        header = ['| Stage | Budget |', '|-------|--------|']
        summary = f'Composed deadline: **{result:g} s**'
        met = round(result, 6) <= analysis.target
    else:
        header, rows, summary, met = _analyze_utilization(analysis)
    verdict = 'met' if met else 'NOT met'
    return ([f'## {analysis.name} (Scenario {analysis.scenario})', ''] +
            header + rows +
            ['', f'{summary}; target {analysis.target:g}: **{verdict}**', ''])


def generate_analysis(model, out):
    lines = [f'# Analysis of {model.name}', '']
    for a in model.analyses:
        lines += analyze(a)
    _write(out, 'analysis.md', lines)


def apply_transformations(model, out):
    os.makedirs(out, exist_ok=True)
    generate_connector_table(model, out)
    generate_view(model, out)
    generate_summary(model, out)
    generate_analysis(model, out)
