import os

from textx import metamodel_from_file, get_location, TextXSemanticError


def _error(message, obj):
    raise TextXSemanticError(message, **get_location(obj))


def _kind(obj):
    return obj.__class__.__name__


def _crosses(link):
    return len({c.system.name for c in link.path}) > 1


def _boundary(connector):
    """A connector is a boundary connector when one of its links joins two
    constituents."""
    return any(_crosses(link) for link in connector.links)


def check_model(model):
    components = [e for e in model.elements if _kind(e) == 'Component']
    connectors = [e for e in model.elements if _kind(e) == 'Connector']

    for k in connectors:
        # C1. Every link joins at least two components.
        for link in k.links:
            if len(link.path) < 2:
                _error(
                    f'{k.name}: a link must join at least two components',
                    k)

        # C2. A control command has a single source with authority over
        # its targets.
        if 'control_command' in k.natures:
            sources = {link.path[0].name for link in k.links}
            if len(sources) > 1:
                _error(
                    f'{k.name}: control command with several sources '
                    f'{sorted(sources)}',
                    k)

        # C3. Every boundary connector is governed by an agreement among
        # owners.
        if _boundary(k) and not k.agreement:
            _error(f'{k.name}: boundary connector without agreement', k)

        # C6. The SoS is acknowledged, not directed: no command crosses a
        # boundary (Delivery 1, 5.5; hierarchical style is internal).
        if _boundary(k) and 'control_command' in k.natures:
            _error(
                f'{k.name}: boundary connector carrying a control command '
                f'(no constituent has command authority over another)',
                k)

        # C7. Gateway pattern: every boundary link starts and ends at a
        # boundary component (tier T2) (Delivery 1, 3.2).
        for link in k.links:
            for a, b in zip(link.path, link.path[1:]):
                if a.system is not b.system and (
                        a.tier != 'T2' or b.tier != 'T2'):
                    bad = a if a.tier != 'T2' else b
                    _error(
                        f'{k.name}: boundary link reaches {bad.name} '
                        f'(tier {bad.tier}); only T2 boundary components '
                        f'may face another constituent',
                        k)

        # C9. Event-oriented style: a notification is published without
        # waiting for the consumer, so it is never blocking.
        if 'event_notification' in k.natures and k.coupling == 'blocking':
            _error(
                f'{k.name}: event notification with blocking coupling '
                f'(the publisher must not wait for the consumer)',
                k)

    # C4. A data store (T4) is accessed by dependency from a single
    # component.
    for c in components:
        if c.tier == 'T4':
            users = {
                link.path[-2].name
                for k in connectors if 'dependency' in k.natures
                for link in k.links if link.path[-1] is c
            }
            if len(users) > 1:
                _error(
                    f'{c.name}: data store shared by {sorted(users)}',
                    c)

    # C8. Hierarchical style and control loop: physical equipment (T5)
    # receives control commands from a single component
    # (Delivery 1, 5.2: "cada equipo recibe comandos de un unico origen").
    for c in components:
        if c.tier == 'T5':
            authorities = {
                link.path[-2].name
                for k in connectors if 'control_command' in k.natures
                for link in k.links if link.path[-1] is c
            }
            if len(authorities) > 1:
                _error(
                    f'{c.name}: equipment commanded by several '
                    f'authorities {sorted(authorities)}',
                    c)

    # C5. Every factor of an analysis is valid for its metric and the
    # element carries the property the analysis needs (an optional number
    # that is not written takes the value 0). A value written in the factor
    # replaces the property of the element.
    for a in model.analyses:
        for f in a.factors:
            kind = _kind(f)
            if kind in ('Group', 'Replicated') and a.metric != 'availability':
                _error(
                    f'{a.name}: a redundant factor only applies to an '
                    f'availability analysis',
                    a)
            if kind == 'Group':
                refs = f.alternatives
            else:
                refs = [f.ref]
            for r in refs:
                if a.metric == 'utilization':
                    missing = [p for p in ('capacity', 'load')
                               if not getattr(r, p)]
                    if missing:
                        _error(
                            f'{a.name}: {r.name} has no '
                            f'{" or ".join(missing)} property',
                            a)
                elif kind == 'Single' and f.value:
                    continue
                elif not getattr(r, a.metric):
                    _error(
                        f'{a.name}: {r.name} has no {a.metric} property',
                        a)


def create_metamodel():
    grammar = os.path.join(os.path.dirname(__file__), 'arch.tx')
    mm = metamodel_from_file(grammar)
    mm.register_model_processor(lambda model, metamodel: check_model(model))
    return mm
