from __future__ import annotations

from typing import TYPE_CHECKING

from flask import g

from enums import Dep, LeafState, ProgressState
#from leaf.models import Leaf

if TYPE_CHECKING:
    from .models import Proj
    from leaf.models import Mango


def b_s5(proj: Proj) -> bool:
    if proj.progress.state is not ProgressState.s0:
        return True
    if proj.progress.freeroles:
        # for leaf in proj.leafs.filter_by(state=Dep.waitting).all():
        #     leaf.state = LeafState.droped_e
        #     leaf.track.append(f'expire|{g.now}')
        return False
    #for leaf in proj.leafs.filter(Leaf.dep.in_((Dep.d51, Dep.d59))).all():
    #    leaf.state = LeafState.normal
    #    leaf.track.append(f'begin|{g.now}')
    proj.progress.state = ProgressState.s5
    return True


def b_s7_1(proj: Proj) -> bool:
    unfinshed = proj.progress.unfinished
    if unfinshed.get(Dep.d51, 0) + unfinshed.get(Dep.d59, 0) > 0:
        return False
    for leaf in proj.leafs.filter_by(dep=Dep.d71).all():
        leaf.state = LeafState.normal
        leaf.track.append(f'begin|{g.now}')
    proj.progress.state = ProgressState.s7_1
    return True


def b_s7_2(proj: Proj) -> bool:
    if proj.progress.unfinished[Dep.d71] > 0:
        return False
    for leaf in proj.leafs.filter_by(dep=Dep.d72).all():
        leaf.state = LeafState.normal
        leaf.track.append(f'begin|{g.now}')
    proj.progress.state = ProgressState.s7_2
    return True


def b_s7_3(proj: Proj) -> bool:
    if proj.progress.unfinished[Dep.d72] > 0:
        return False
    for leaf in proj.leafs.filter_by(dep=Dep.d73).all():
        leaf.state = LeafState.normal
        leaf.track.append(f'begin|{g.now}')
    proj.progress.state = ProgressState.s7_3
    return True


def plus_complexity(proj: Proj, dep: Dep, mango: Mango) -> None:
    if dep // 10 == 5:
        proj.complexity['al'][mango.id[:9]] = mango.metainfo['duration']
    elif dep == 60:
        proj.complexity['pc'] += 1
    elif dep == 71:
        proj.complexity['cl'][mango.id[:9]] = mango.metainfo['duration']


def minus_complexity(proj: Proj, dep: Dep, mango: Mango) -> None:
    if dep // 10 == 5:
        proj.complexity['al'].pop(mango.id[:9])
    elif dep == 60:
        proj.complexity['pc'] -= 1
    elif dep == 71:  # self.dep // 10 == 7:
        proj.complexity['cl'].pop(mango.id[:9])


def run_elfs(proj: Proj, dep: Dep, mango: Mango, pos: bool) -> None:
    if pos is None:
        b_s5(proj)
        return

    if dep // 10 == 5:
        b_s7_1(proj)
    elif dep == Dep.d71:
        b_s7_2(proj)
    elif dep == Dep.d72:
        b_s7_3(proj)

    if pos:
        plus_complexity(proj, dep, mango)
        proj.progress.unfinished[dep] -= 1
    else:
        minus_complexity(proj, dep, mango)
        proj.progress.unfinished[dep] += 1
