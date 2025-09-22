import numpy as np
import matplotlib as mpl
from matplotlib.colors import to_rgb, to_rgba
from numpy.testing import assert_array_equal


USE_PROPS = [
    "alpha",
    "edgecolor",
    "facecolor",
    "fill",
    "hatch",
    "height",
    "linestyle",
    "linewidth",
    "paths",
    "xy",
    "xydata",
    "sizes",
    "zorder",
]


def assert_artists_equal(list1, list2):

    assert len(list1) == len(list2)
    for a1, a2 in zip(list1, list2):
        assert a1.__class__ == a2.__class__
        prop1 = a1.properties()
        prop2 = a2.properties()
        for key in USE_PROPS:
            if key not in prop1:
                continue
            v1 = prop1[key]
            v2 = prop2[key]
            if key == "paths":
                for p1, p2 in zip(v1, v2):
                    assert_array_equal(p1.vertices, p2.vertices)
                    assert_array_equal(p1.codes, p2.codes)
            elif key == "color":
                v1 = mpl.colors.to_rgba(v1)
                v2 = mpl.colors.to_rgba(v2)
                assert v1 == v2
            elif isinstance(v1, np.ndarray):
                assert_array_equal(v1, v2)
            else:
                assert v1 == v2


def assert_legends_equal(leg1, leg2):

    assert leg1.get_title().get_text() == leg2.get_title().get_text()
    for t1, t2 in zip(leg1.get_texts(), leg2.get_texts()):
        assert t1.get_text() == t2.get_text()

    assert_artists_equal(
        leg1.get_patches(), leg2.get_patches(),
    )
    assert_artists_equal(
        leg1.get_lines(), leg2.get_lines(),
    )


def assert_plots_equal(ax1, ax2, labels=True):

    assert_artists_equal(ax1.patches, ax2.patches)
    assert_artists_equal(ax1.lines, ax2.lines)
    assert_artists_equal(ax1.collections, ax2.collections)

    if labels:
        assert ax1.get_xlabel() == ax2.get_xlabel()
        assert ax1.get_ylabel() == ax2.get_ylabel()

def assert_plots_all_equal(ax1, ax2, labels=True, tol=1e-5, rtol=1e-3):
    # Core artists
    assert_artists_equal(ax1.patches, ax2.patches)
    assert_artists_equal(ax1.lines, ax2.lines)
    assert_artists_equal(ax1.collections, ax2.collections)
    assert_artists_equal(ax1.images, ax2.images)
    assert_artists_equal(ax1.texts, ax2.texts)

    # Titles and labels
    if labels:
        # assert ax1.get_title() == ax2.get_title()
        assert ax1.get_xlabel() == ax2.get_xlabel()
        assert ax1.get_ylabel() == ax2.get_ylabel()

        # Axis scales/limits
        assert ax1.get_xscale() == ax2.get_xscale()
        assert ax1.get_yscale() == ax2.get_yscale()
        assert np.allclose(ax1.get_xlim(), ax2.get_xlim(), rtol=rtol, atol=tol)
        assert np.allclose(ax1.get_ylim(), ax2.get_ylim(), rtol=rtol, atol=tol)
        assert ax1.get_aspect() == ax2.get_aspect()

        # Ticks
        assert np.allclose(ax1.get_xticks(), ax2.get_xticks(), rtol=rtol, atol=tol)
        assert np.allclose(ax1.get_yticks(), ax2.get_yticks(), rtol=rtol, atol=tol)
        assert [t.get_text() for t in ax1.get_xticklabels()] == [t.get_text() for t in ax2.get_xticklabels()]
        assert [t.get_text() for t in ax1.get_yticklabels()] == [t.get_text() for t in ax2.get_yticklabels()]

        # Spines
        for k in ax1.spines:
            s1, s2 = ax1.spines[k], ax2.spines[k]
            # assert s1.get_visible() == s2.get_visible()
            assert_colors_equal(s1.get_edgecolor(), s2.get_edgecolor())
            assert np.isclose(s1.get_linewidth(), s2.get_linewidth(), rtol=rtol, atol=tol)

        # Legend
        leg1, leg2 = ax1.get_legend(), ax2.get_legend()
        # assert (leg1 is None) == (leg2 is None)
        if leg1 is not None and leg2 is not None: assert_legends_equal(leg1, leg2)

        # Gridlines
        gl1x, gl2x = ax1.get_xgridlines(), ax2.get_xgridlines()
        gl1y, gl2y = ax1.get_ygridlines(), ax2.get_ygridlines()
        assert len(gl1x) == len(gl2x) and len(gl1y) == len(gl2y)

def assert_colors_equal(a, b, check_alpha=True):

    def handle_array(x):

        if isinstance(x, np.ndarray):
            if x.ndim > 1:
                x = np.unique(x, axis=0).squeeze()
            if x.ndim > 1:
                raise ValueError("Color arrays must be 1 dimensional")
        return x

    a = handle_array(a)
    b = handle_array(b)

    f = to_rgba if check_alpha else to_rgb
    assert f(a) == f(b)
