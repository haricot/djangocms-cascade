import pytest
from cmsplugin_cascade.bootstrap4.grid import (Bootstrap4Container, Bootstrap4Row, Bootstrap4Column, BootstrapException,
                                               Breakpoint, Bound)

def test_xs_cols():
    container = Bootstrap4Container()
    row = container.add_row(Bootstrap4Row())
    for _ in range(3):
        row.add_column(Bootstrap4Column('col'))
    row.compute_column_bounds()


def test_xs_cols_with_flex():
    container = Bootstrap4Container()
    row = container.add_row(Bootstrap4Row())
    row.add_column(Bootstrap4Column('col-3'))
    row.add_column(Bootstrap4Column('col'))
    row.add_column(Bootstrap4Column('col'))
    row.compute_column_bounds()
    assert row[0].get_bound(Breakpoint.xs) == Bound(80.0, 143.0)
    assert row[0].get_bound(Breakpoint.sm) == Bound(135.0, 135.0)
    assert row[0].get_bound(Breakpoint.md) == Bound(180.0, 180.0)
    assert row[0].get_bound(Breakpoint.lg) == Bound(240.0, 240.0)
    assert row[0].get_bound(Breakpoint.xl) == Bound(285.0, 285.0)

    assert row[1].get_bound(Breakpoint.xs) == Bound(120.0, 214.5)
    assert row[1].get_bound(Breakpoint.sm) == Bound(202.5, 202.5)
    assert row[1].get_bound(Breakpoint.md) == Bound(270.0, 270.0)
    assert row[1].get_bound(Breakpoint.lg) == Bound(360.0, 360.0)
    assert row[1].get_bound(Breakpoint.xl) == Bound(427.5, 427.5)
# Sample xs vw 572 : col3 + col + col: 143 + 214.5 + 214.5 = 572


def test_xs_cols_with_auto_and_flex():
    container = Bootstrap4Container()
    row = container.add_row(Bootstrap4Row())
    row.add_column(Bootstrap4Column('col-3'))
    row.add_column(Bootstrap4Column('col-auto'))
    row.add_column(Bootstrap4Column('col'))
    row.compute_column_bounds()
    assert row[0].get_bound(Breakpoint.xs) == Bound(80.0, 143.0)
    assert row[0].get_bound(Breakpoint.sm) == Bound(135.0, 135.0)
    assert row[0].get_bound(Breakpoint.md) == Bound(180.0, 180.0)
    assert row[0].get_bound(Breakpoint.lg) == Bound(240.0, 240.0)
    assert row[0].get_bound(Breakpoint.xl) == Bound(285.0, 285.0)

    assert row[1].get_bound(Breakpoint.xs) == Bound(30.0, 399.0)
    assert row[1].get_bound(Breakpoint.sm) == Bound(30.0, 375.0)
    assert row[1].get_bound(Breakpoint.md) == Bound(30.0, 510.0)
    assert row[1].get_bound(Breakpoint.lg) == Bound(30.0, 690.0)
    assert row[1].get_bound(Breakpoint.xl) == Bound(30.0, 825.0)

    assert row[2].get_bound(Breakpoint.xs) == Bound(30.0, 399.0)
    assert row[2].get_bound(Breakpoint.sm) == Bound(30.0, 375.0)
    assert row[2].get_bound(Breakpoint.md) == Bound(30.0, 510.0)
    assert row[2].get_bound(Breakpoint.lg) == Bound(30.0, 690.0)
    assert row[2].get_bound(Breakpoint.xl) == Bound(30.0, 825.0)
# Sample xs vw 572 : col-3 + col-auto + col : 143 + 399 + 30 = 572


def test_mix_flex_with_fixed():
    row = Bootstrap4Row()
    with pytest.raises(BootstrapException):
        row.add_column(Bootstrap4Column('col col-1'))


def test_mix_flex_with_auto():
    row = Bootstrap4Row()
    with pytest.raises(BootstrapException):
        row.add_column(Bootstrap4Column('col col-auto'))


def test_mix_fixed_with_auto():
    row = Bootstrap4Row()
    with pytest.raises(BootstrapException):
        row.add_column(Bootstrap4Column('col-1 col-auto'))


def test_growing_columns():
    container = Bootstrap4Container()
    row = container.add_row(Bootstrap4Row())
    row.add_column(Bootstrap4Column('col-12 col-sm-6 col-lg-4'))
    row.add_column(Bootstrap4Column('col-12 col-sm-6 col-lg-4'))
    row.add_column(Bootstrap4Column('col-12 col-sm-12 col-lg-4'))
    row.compute_column_bounds()
    assert row[0].get_bound(Breakpoint.xs) == Bound(320.0, 572.0)
    assert row[0].get_bound(Breakpoint.sm) == Bound(270.0, 270.0)
    assert row[0].get_bound(Breakpoint.md) == Bound(360.0, 360.0)
    assert row[0].get_bound(Breakpoint.lg) == Bound(320.0, 320.0)
    assert row[0].get_bound(Breakpoint.xl) == Bound(380.0, 380.0)

    assert row[2].get_bound(Breakpoint.xs) == Bound(320.0, 572.0)
    assert row[2].get_bound(Breakpoint.sm) == Bound(540.0, 540.0)
    assert row[2].get_bound(Breakpoint.md) == Bound(720.0, 720.0)
    assert row[2].get_bound(Breakpoint.lg) == Bound(320.0, 320.0)
    assert row[2].get_bound(Breakpoint.xl) == Bound(380.0, 380.0)


def test_nicolas():
    container = Bootstrap4Container()
    row = container.add_row(Bootstrap4Row())
    row.add_column(Bootstrap4Column('col'))
    row.add_column(Bootstrap4Column('col-auto'))
    row.add_column(Bootstrap4Column('col-2'))
    row.compute_column_bounds()
    assert row[0].get_bound(Breakpoint.xs) == Bound(30.0, 446.7) # still needs to round
    assert row[0].get_bound(Breakpoint.sm) == Bound(30.0, 420.0)
    assert row[0].get_bound(Breakpoint.md) == Bound(30.0, 570.0)
    assert row[0].get_bound(Breakpoint.lg) == Bound(30.0, 770.0)
    assert row[0].get_bound(Breakpoint.xl) == Bound(30.0, 920.0)

    assert row[1].get_bound(Breakpoint.xs) == Bound(30.0, 446.7)
    assert row[1].get_bound(Breakpoint.sm) == Bound(30.0, 420.0)
    assert row[1].get_bound(Breakpoint.md) == Bound(30.0, 570.0)
    assert row[1].get_bound(Breakpoint.lg) == Bound(30.0, 770.0)
    assert row[1].get_bound(Breakpoint.xl) == Bound(30.0, 920.0)

    assert row[2].get_bound(Breakpoint.xs) == Bound(53.3, 95.3)
    assert row[2].get_bound(Breakpoint.sm) == Bound(90.0, 90.0)
    assert row[2].get_bound(Breakpoint.md) == Bound(120.0, 120.0)
    assert row[2].get_bound(Breakpoint.lg) == Bound(160.0, 160.0)
    assert row[2].get_bound(Breakpoint.xl) == Bound(190.0, 190.0)
# Sample vw 572px : col + col-auto + col-2 : 446.7 + 30 + 95.3 = 572


def test4_cols_with_auto_and_fixed():
    container = Bootstrap4Container()
    row = container.add_row(Bootstrap4Row())
    row.add_column(Bootstrap4Column('col-auto'))
    row.add_column(Bootstrap4Column('col-auto'))
    row.add_column(Bootstrap4Column('col-auto'))
    row.add_column(Bootstrap4Column('col-5'))
    row.compute_column_bounds()
    assert row[0].get_bound(Breakpoint.xs) == Bound(30.0, 273.7)
    assert row[0].get_bound(Breakpoint.sm) == Bound(30.0, 255.0)
    assert row[0].get_bound(Breakpoint.md) == Bound(30.0, 360.0)
    assert row[0].get_bound(Breakpoint.lg) == Bound(30.0, 500.0)
    assert row[0].get_bound(Breakpoint.xl) == Bound(30.0, 605.0)

    assert row[3].get_bound(Breakpoint.xs) == Bound(133.3, 238.3)
    assert row[3].get_bound(Breakpoint.sm) == Bound(225.0, 225.0)
    assert row[3].get_bound(Breakpoint.md) == Bound(300.0, 300.0)
    assert row[3].get_bound(Breakpoint.lg) == Bound(400.0, 400.0)
    assert row[3].get_bound(Breakpoint.xl) == Bound(475.0, 475.0)
# Sample xl vw 1140 : col-auto + col-auto + col-auto + col-5: 605.0 + 30.0 + 30.0 + 475= 1140


def test5_growing_columns():
    container = Bootstrap4Container()
    row = container.add_row(Bootstrap4Row())
    row.add_column(Bootstrap4Column('col-12 col-sm-auto col-lg-4'))
    row.add_column(Bootstrap4Column('col-12 col-sm-7 col-lg-4'))
    row.add_column(Bootstrap4Column('col-12 col-sm-2 col-lg-4'))
    row.compute_column_bounds()
    assert row[0].get_bound(Breakpoint.xs) == Bound(320, 572.0)
    assert row[0].get_bound(Breakpoint.sm) == Bound(30.0, 135.0)
    assert row[0].get_bound(Breakpoint.md) == Bound(30.0, 180.0)
    assert row[0].get_bound(Breakpoint.lg) == Bound(320.0, 320.0)
    assert row[0].get_bound(Breakpoint.xl) == Bound(380.0, 380.0)

    assert row[1].get_bound(Breakpoint.xs) == Bound(320.0, 572.0)
    assert row[1].get_bound(Breakpoint.sm) == Bound(315.0, 315.0)
    assert row[1].get_bound(Breakpoint.md) == Bound(420.0, 420.0)
    assert row[1].get_bound(Breakpoint.lg) == Bound(320.0, 320.0)
    assert row[1].get_bound(Breakpoint.xl) == Bound(380.0, 380.0)

    assert row[2].get_bound(Breakpoint.xs) == Bound(320.0, 572.0)
    assert row[2].get_bound(Breakpoint.sm) == Bound(90.0, 90.0)
    assert row[2].get_bound(Breakpoint.md) == Bound(120.0, 120.0)
    assert row[2].get_bound(Breakpoint.lg) == Bound(320.0, 320.0)
    assert row[2].get_bound(Breakpoint.xl) == Bound(380.0, 380.0)
# Sample sm vw 540 : col-sm-auto + col-sm-7 + col-sm-2 : 135.0 + 315.0 + 90 = 540
