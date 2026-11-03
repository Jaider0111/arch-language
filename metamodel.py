import os
from textx import metamodel_from_file, get_location, TextXSemanticError


def _error(message, obj):
    raise TextXSemanticError(message, **get_location(obj))


def _crosses(link):
    return len({c.system.name for c in link.path}) > 1


def _boundary(connector):
    """A connector is a boundary connector when one of its links joins two constituents."""
    return any(_crosses(link) for link in connector.links)


def _singles(factor):
    return factor.members if factor.__class__.__name__ == 'Group' else [factor]


def check_model(model):
    components = [e for e in model.elements if e.__class__.__name__ == 'Component']
    connectors = [e for e in model.elements if e.__class__.__name__ == 'Connector']

    for k in connectors:
        # C1. Every link joins at least two components.
        for link in k.links:
            if len(link.path) < 2:
                _error(f'{k.name}: a link must join at least two components', k)
        # C2. A control command has a single source with authority over its targets.
        if 'control_command' in k.natures:
            sources = {link.path[0].name for link in k.links}
            if len(sources) > 1:
                _error(f'{k.name}: control command with several sources {sorted(sources)}', k)
        # C3. Every boundary connector is governed by an agreement among owners.
        if _boundary(k) and not k.agreement:
            _error(f'{k.name}: boundary connector without agreement', k)
        # C6 [D]. Layers (NCS, Delivery 1 section 5): no component of T1 is
        # joined directly to a data store of T4; every read goes through a T3 service.
        for link in k.links:
            for a, b in zip(link.path, link.path[1:]):
                if {a.tier, b.tier} == {'T1', 'T4'}:
                    _error(f'{k.name}: {a.name} ({a.tier}) joined directly to {b.name} ({b.tier})', k)
        # C7 [D]. Acknowledged SoS (global styles, Delivery 1): a control command
        # never crosses a boundary; authority exists only inside one constituent.
        if 'control_command' in k.natures and _boundary(k):
            _error(f'{k.name}: control command crosses the boundary of a constituent', k)

    # C4 [D, adapted]. A data store (T4) is accessed by dependency only from components
    # of its own domain. A store without domain keeps the rule of Laboratory 4:
    # a single component.
    for c in components:
        if c.tier == 'T4':
            users = [link.path[-2]
                     for k in connectors if 'dependency' in k.natures
                     for link in k.links if link.path[-1] is c]
            if c.domain:
                foreign = sorted({u.name for u in users if u.domain != c.domain})
                if foreign:
                    _error(f'{c.name}: data store of domain {c.domain} accessed from {foreign}', c)
            elif len({u.name for u in users}) > 1:
                _error(f'{c.name}: data store shared by {sorted({u.name for u in users})}', c)

    # C5 [D, extended]. Every factor of an analysis carries the property the analysis needs
    # (an optional number that is not written takes the value 0).
    for a in model.analyses:
        for f in a.factors:
            for s in _singles(f):
                r = s.ref
                if a.metric in ('availability', 'latency') and not getattr(r, a.metric):
                    _error(f'{a.name}: {r.name} has no {a.metric} property', a)
                if a.metric == 'availability' and s.beta and (getattr(r, 'instances', 0) or 1) < 2:
                    _error(f'{a.name}: {r.name} has beta but fewer than 2 instances', a)
                if a.metric == 'deadline' and not s.value:
                    _error(f'{a.name}: {r.name} has no budget (= value) for the deadline', a)
                if a.metric == 'recovery':
                    if r.__class__.__name__ != 'Component' or not r.event_capacity or not r.event_load:
                        _error(f'{a.name}: {r.name} needs event_capacity and event_load', a)
        if a.metric == 'recovery' and not a.backlog:
            _error(f'{a.name}: a recovery analysis needs its backlog', a)


def create_metamodel():
    grammar = os.path.join(os.path.dirname(__file__), 'arch.tx')
    mm = metamodel_from_file(grammar)
    mm.register_model_processor(lambda model, metamodel: check_model(model))
    return mm
